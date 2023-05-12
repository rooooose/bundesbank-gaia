import json

def write_stats(year, i, doubt_count_total):

  with open('doubt_results_' + i + '.json','r') as file:
        try:
          file_data = json.load(file)
          doubt_count_year = len(file_data[year])
        except:
          file_data = {}
          doubt_count_year = 0

        

  with open('found_results_' + i + '.json','r') as file:
        try:
          file_data = json.load(file)
          found_count_year = len(file_data[year])
        except:
          file_data = {}
          found_count_year = 0


  to_find_per_year = doubt_count_year + found_count_year
  doubt_count_total += doubt_count_year

  found_per_year = found_count_year*100/to_find_per_year
  #conclusions_found.append(year + " : " + str(found_per_year) + "% were found\n")
  conclusion_found = year + " : " + str(found_per_year) + "% were found\n"
  conclusion_doubt = str(doubt_count_total) + " doubtful results until now"


  # for percentage in conclusions_found :
  #   write_file.write(percentage)

  f = open('stats' + i + '.txt','a+')
  f.write(conclusion_found)
  text = f.read()
  f.write(conclusion_doubt+'\n')

  
  # writing the data into the files
  # with open('doubtful_results_' + str(i) + '.txt','w') as write_file:
  #   write_file.write(conclusion_doubt)
  #   json.dump(doubt_list, write_file, indent=4)
  # with open('found_results_' + str(i) + '.txt','w') as write_file: 
  #   for percentage in conclusions_found :
  #       write_file.write(percentage)
  #   json.dump(found_list, write_file, indent=4)
  
  return doubt_count_total


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