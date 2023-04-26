import json

def write_result_files(year, i, found_list, doubt_list, conclusions_found, doubt_count):

    to_find_per_year = len(doubt_list[str(year)]) + len(found_list[str(year)])
    doubt_count += len(doubt_list[str(year)])

    found_per_year = len(found_list[str(year)])*100/to_find_per_year
    conclusions_found.append(str(year) + " : " + str(found_per_year) + "% were found\n")
    conclusion_doubt = str(doubt_count) + " might be wrong :"

    
    # writing the data into the files
    with open('doubtful_results_' + str(i) + '.txt','w') as write_file:
      write_file.write(conclusion_doubt)
      json.dump(doubt_list, write_file, indent=4)
    with open('found_results_' + str(i) + '.txt','w') as write_file: 
      for percentage in conclusions_found :
          write_file.write(percentage)
      json.dump(found_list, write_file, indent=4)
    
    return doubt_count
