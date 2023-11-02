def get_timestamps():
  try:
   time_element=driver.find_element(By.TAG_NAME, 'time')
   date=(time_element.get_attribute('datetime'))
   time.append(date)
  except:
    date='unknown'
    time.append(date)
    print('no date')

def get_bbc_news():
    pass