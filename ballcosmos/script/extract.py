import re

SCANNING_REGULAR_EXPRESSION = re.compile("(?:\"(?:[^\\\"]|\\.)*\") | (?:'(?:[^\\']|\\.)*') | (?:\[.*\]) | \S+", re.VERBOSE)

SPLIT_WITH_REGEX = re.compile("\s+with\s+", re.IGNORECASE)

# Regular expression to identify a String as a floating point number
FLOAT_CHECK_REGEX = re.compile("\A\s*[-+]?\d*\.\d+\s*\Z")

# Regular expression to identify a String as a floating point number in
# scientific notation
SCIENTIFIC_CHECK_REGEX = re.compile("\A\s*[-+]?(\d+((\.\d+)?)|(\.\d+))[eE][-+]?\d+\s*\Z")

# Regular expression to identify a String as an integer
INT_CHECK_REGEX = re.compile("\A\s*[-+]?\d+\s*\Z")

# Regular expression to identify a String as an integer in hexadecimal format
HEX_CHECK_REGEX = re.compile("\A\s*0[xX][\dabcdefABCDEF]+\s*\Z")

# Regular expression to identify a String as an Array of numbers
ARRAY_CHECK_REGEX = re.compile("\A\s*\[.*\]\s*\Z")

def remove_quotes(string):
  """Returns the string with leading and trailing quotes removed"""
  if (string.startswith('"') and string.endswith('"')) or (string.startswith("'") and string.endswith("'")):
    return string[1:-1]
  else:
    return string

def is_float(string):
  """Returns whether the String represents a floating point number"""
  if FLOAT_CHECK_REGEX.match(string) or SCIENTIFIC_CHECK_REGEX.match(string):
    return True
  else:
    return False

def is_int(string):
  """Returns whether the String represents an integer"""
  if INT_CHECK_REGEX.match(string):
    return True
  else:
    return False

def is_hex(string):
  """Whether the String represents a hexadecimal number"""
  if HEX_CHECK_REGEX.match(string):
    return True
  else:
    return False

def is_array(string):
  """Whether the String represents an Array"""
  if ARRAY_CHECK_REGEX.match(string):
    return True
  else:
    return False

def convert_to_value(string):
  """Converts the String into either a Float, Integer, or Array
  depending on what the String represents. It can successfully convert
  floating point numbers in both fixed and scientific notation, integers
  in hexadecimal notation, and Arrays. If it can not be converted into
  any of the above then the original String is returned.
  """
  return_value = string
  try:
    if is_float(string):
      # Floating Point in normal or scientific notation
      return_value = float(string)
    elif is_int(string):
      # Integer
      return_value = int(string)
    elif is_hex(string):
      # Hex
      return_value = int(string)
    elif self.is_array:
      # Array
      return_value = eval(string)
  except Exception:
    # Something went wrong so just return the string as is
    pass
  return return_value

def add_cmd_parameter(keyword, value, cmd_params):
  quotes_removed = remove_quotes(value)
  if value == quotes_removed:
    cmd_params[keyword] = convert_to_value(value)
  else:
    cmd_params[keyword] = quotes_removed

def extract_fields_from_cmd_text(text):
  split_string = re.split(SPLIT_WITH_REGEX, text, 2)
  if len(split_string) == 1 and SPLIT_WITH_REGEX.match(text):
    raise RuntimeError("ERROR: 'with' must be followed by parameters : {:s}".format(text))

  # Extract target_name and cmd_name
  first_half = split_string[0].split(" ")
  if len(first_half) < 2:
    raise RuntimeError("ERROR: Both Target Name and Command Name must be given : {:s}".format(text))
  if len(first_half) > 2:
    raise RuntimeError("ERROR: Only Target Name and Command Name must be given before 'with' : {:s}".format(text))
  target_name = first_half[0]
  cmd_name = first_half[1]
  cmd_params = {}

  if len(split_string) == 2:
    # Extract Command Parameters
    second_half = SCANNING_REGULAR_EXPRESSION.findall(split_string[1])
    keyword = None
    value = None
    comma = None
    for item in second_half:
      if not keyword:
        keyword = item
        continue
      if not value:
        if item.endswith(','):
          value = item[0:-1]
          comma = True
        else:
          value = item
          continue
      if not comma:
        if item != ',':
          raise RuntimeError("Missing comma in command parameters: {:s}".format(text))
      add_cmd_parameter(keyword, value, cmd_params)
      keyword = None
      value = None
      comma = None
    if keyword:
      if value:
        add_cmd_parameter(keyword, value, cmd_params)
      else:
        raise RuntimeError("Missing value for last command parameter: {:s}".format(text))

  return [target_name, cmd_name, cmd_params]

def extract_fields_from_tlm_text(text):
  split_string = text.split(" ")
  if len(split_string) != 3:
    raise RuntimeError("ERROR: Telemetry Item must be specified as 'TargetName PacketName ItemName' : {:s}".format(text))
  target_name = split_string[0]
  packet_name = split_string[1]
  item_name = split_string[2]
  return [target_name, packet_name, item_name]

def extract_fields_from_set_tlm_text(text):
  error_msg = "ERROR: Set Telemetry Item must be specified as 'TargetName PacketName ItemName = Value' : {:s}".format(text)
  # We have to handle these cases:
  # set_tlm("TGT PKT ITEM='new item'")
  # set_tlm("TGT PKT ITEM = 'new item'")
  # set_tlm("TGT PKT ITEM= 'new item'")
  # set_tlm("TGT PKT ITEM ='new item'")
  split_string = text.split('=')
  if len(split_string) < 2 or not split_string[1].strip():
    raise error_msg
  split_string = split_string[0].strip().split(" ") + '='.join(split_string[1:]).strip()
  if len(split_string) != 4: # Ensure tgt,pkt,item,value
    raise error_msg
  target_name = split_string[0]
  packet_name = split_string[1]
  item_name = split_string[2]
  value = convert_to_value(split_string[3].strip())
  if isinstance(value, str):
    value = remove_quotes(value)
  return [target_name, packet_name, item_name, value]

def extract_fields_from_check_text(text):
  split_string = text.split(" ")
  if len(split_string) < 3:
    raise RuntimeError("ERROR: Check improperly specified: {:s}")
  target_name = split_string[0]
  packet_name = split_string[1]
  item_name = split_string[2]
  comparison_to_eval = None
  if len(split_string) == 3:
    return [target_name, packet_name, item_name, comparison_to_eval]
  if len(split_string) < 4:
    raise RuntimeError("ERROR: Check improperly specified: {:s}".format(text))
  comparison_to_eval = " ".join(split_string[3:])
  if split_string[3] == '=':
    raise RuntimeError("ERROR: Use '==' instead of '=': {:s}")
  return [target_name, packet_name, item_name, comparison_to_eval]
