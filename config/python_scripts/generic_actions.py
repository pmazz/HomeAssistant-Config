def log_info(logger, data, msg):
  log_enabled = str(data.get("log_enabled", "false"))
  if log_enabled.lower() == "true":
    logger.debug(msg)

def log_error(logger, msg):
  logger.error(msg)

def string2json(json_string):
  #Remove spaces
  json_string = json_string.strip()
  #Remove { and }
  json_string = json_string.lstrip("{").rstrip("}")
  #Split the string based on ','
  json_items = json_string.split(",")
  #Create the dictionary
  json_obj = {}
  for item in json_items:
    #Split the item based on ':'
    keyvalue = item.split(":")
    if len(keyvalue) == 2:
      #Remove spaces and quotes
      k = keyvalue[0].strip("' \"")
      v = keyvalue[1].strip("' \"")
      json_obj[k] = v
  #Return the dictionary
  return json_obj

#Execute requested action
action = data.get("action", "")

#Notify start script execution
log_info(logger, data, "STARTING script -> generic_actions.py -> {}".format(action))

if action.lower() == "time.sleep":
#Action -> time.sleep
#Parameter 1 -> seconds
#Parameter 2 -> log_enabled
  #Executing time.sleep function
  seconds_str = data.get("seconds", "")
  if seconds_str.isnumeric():
    seconds = int(seconds_str)
    if seconds > 0:
      log_info(logger, data, "Executing 'time.sleep({})'...".format(seconds))
      time.sleep(seconds)
    else:
      log_error(logger, "Cannot execute 'sleep' action: 'seconds' parameter has an invalid value ({}).".format(seconds))
  else:
    log_error(logger, "Cannot execute 'sleep' action: 'seconds' parameter is not a number ({}).".format(seconds_str))

elif action.lower() == "exec_ha_service":
#Action -> exec_ha_service
#Parameter 1 -> domain
#Parameter 2 -> service
#Parameter 3 -> data
#Parameter 4 -> log_enabled
  #Getting domain and service name
  domain = data.get("domain", "")
  service = data.get("service", "")
  if domain == "":
    log_error(logger, "Parameter 'domain' NOT provided. Script NOT executed.")
  elif service == "":
    log_error(logger, "Parameter 'service' NOT provided. Script NOT executed.")
  else:
    #Getting service data
    service_data_str = data.get("data", "")
    service_data = string2json(service_data_str)
    del service_data["ha_domain"]
    del service_data["ha_service"]
    if "ha_notify" in service_data:
      del service_data["ha_notify"]
    #Execute the service
    log_info(logger, data, "  Service to execute: '{}.{}'".format(domain, service))
    log_info(logger, data, "    Service data: {}".format(service_data))
    hass.services.call(domain, service, service_data, False)

else:
  log_error(logger, "Invalid action specified. Expected: 'time.sleep', 'exec_ha_service'.")

#Notify end script execution
log_info(logger, data, "ENDING script -> generic_actions.py")
