import json

def write_stats(year, i):

  with open('doubt_results_' + i + '.json','r') as file:
    try:
      file_data = json.load(file)

    except:
      file_data = {}
      # doubt_count_total = 0
    
    if year in file_data.keys():
      doubt_count_year = len(file_data[year])
    else:
      doubt_count_year = 0

    doubt_count_total = sum(len(list) for list in file_data.values())


  with open('found_results_' + i + '.json','r') as file:
        try:
          file_data = json.load(file)
          found_count_year = len(file_data[year])
        except:
          file_data = {}
          found_count_year = 0
  
  to_find_per_year = doubt_count_year + found_count_year
  # doubt_count_total += doubt_count_year


  found_per_year = found_count_year*100/to_find_per_year

  conclusion_found = year + " : " + str(found_per_year) + "% were found\n"
  conclusion_doubt = str(doubt_count_total) + " doubtful results until now"
  
  if i == "1" :
  
    with open('exception_at_download.json','r') as file:
      try:
        file_data = json.load(file)
        
      except:
        file_data = {}
    
      if year in file_data.keys():
        exception_count_year = len(file_data[year])
      else:
        exception_count_year = 0

      exception_count_total = sum(len(list) for list in file_data.values())

    # exception_count_total += exception_count_year
    exception_per_year = exception_count_year*100/to_find_per_year
    percentage_except = str(exception_per_year) + "% couldn't be downloaded\n"
    count_except = str(exception_count_total) + " exceptions until now"
  

  f = open('stats' + i + '.txt','a+')
  f.write(conclusion_found)
  f.write(conclusion_doubt+'\n')

  if i == "1" :
    f.write(percentage_except)
    f.write(count_except +'\n\n')
  #   return doubt_count_total, exception_count_total
  # else :
  #   return doubt_count_total
  
  


def write_json(new_data, filename, year):
    
  with open(filename,'r+') as file:
      # First we load existing data into a dict.
      try:
        file_data = json.load(file)
      except:
        file_data = {}

      if year not in file_data.keys():
        file_data[year] = [] 
      
      file_data[year].append(new_data)
      # Sets file's current position at offset.
      file.seek(0)
      # convert back to json.
      json.dump(file_data, file, indent = 4)