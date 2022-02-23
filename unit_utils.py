from astropy import units as u


def convert_to_target_units(x,target_units=u.imperial.ft):
  """
      converts to the target unit and just gives the value as a float
  """
  return x.to(target_units).value

