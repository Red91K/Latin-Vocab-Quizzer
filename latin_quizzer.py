from termcolor import colored
import random
import json
import os

SETTINGS = {}
SETTINGS_PATH = ".config/.settings.json"
def load_settings(config_file_path:str = SETTINGS_PATH):
   global SETTINGS 
   with open(config_file_path,"r") as f:
      SETTINGS = json.load(f) 
   SETTINGS["DefaultVocabFilePath"] = os.path.join(SETTINGS["ListsFolderPath"], SETTINGS["DefaultVocabFile"])
   SETTINGS["MissedWordPath"] = os.path.join(SETTINGS["ConfigPath"], ".missed_words.txt")

class Latin_Word:
   def __init__(self, unformatted_word:str):
      word_str = unformatted_word.split("-")[0]
      word_ar = [component.rstrip(" ").lstrip(" ") for component in word_str.split(",")]

      try:
         def_str = unformatted_word.split("-")[1]
         def_ar = [component.rstrip(" ").lstrip(" ") for component in def_str.split(",")]
      except IndexError: # if user hasn't entered a "-"
         def_ar = []
      
      self.unformatted_word = unformatted_word
      self.word_ar = word_ar
      self.def_ar = def_ar
      # ex: ago, agere, egi, actus,a,um, 3 - to do, lead, drive, act
      # -----------Word-------------------   --------Definition-----
      # Word order needs to be exact         Definition order can change
   
   def __eq__(self, other):
      word_is_equal = [i.lower() for i in self.word_ar] == [i.lower() for i in other.word_ar]
      # for word definition, order should not matter
      def_is_equal = sorted([i.lower() for i in self.def_ar]) == sorted([i.lower() for i in other.def_ar])
      return word_is_equal and def_is_equal
   
   def __str__(self):
      out_str = ""
      for i in range(len(self.word_ar)):
         out_str += f'{self.word_ar[i]}{", " * (i < len(self.word_ar) - 1)}'
         
      out_str += " - "

      for i in range(len(self.def_ar)):
         out_str += f'{self.def_ar[i]}{", " * (i < len(self.def_ar) - 1)}'
      return out_str

   def to_str(self, colored_ar:list = [], color = False):
      if color:
         colored_word_ar = colored_ar[0]
         colored_def_ar = colored_ar[1]

      out_str = ""

      for i in range(len(self.word_ar)):
         if color and i in colored_word_ar:
            out_str += colored(f'{self.word_ar[i]}{", " * (i < len(self.word_ar) - 1)}',color)
         else:  
            out_str += f'{self.word_ar[i]}{", " * (i < len(self.word_ar) - 1)}'
         
      out_str += " - "

      for i in range(len(self.def_ar)):
         if color and i in colored_def_ar:
            out_str += colored(f'{self.def_ar[i]}{", " * (i < len(self.def_ar) - 1)}',color)
         else:
            out_str += f'{self.def_ar[i]}{", " * (i < len(self.def_ar) - 1)}'
      return out_str
   
   # returns mismatches relative to self
   def return_mismatches(self, other) -> [[int], [int]]:
      word_mismatch_ar = []   # will contain indexes of mismatching word components
      self_word_ar = [i.lower() for i in self.word_ar]
      other_word_ar = [i.lower() for i in other.word_ar]

      # iterate through self's word_ar,
      for i in range(min(len(self_word_ar), len(other_word_ar))):
         # if a mismatch is found, add the index of the mismatch to 
         if self_word_ar[i] != other_word_ar[i]:
            word_mismatch_ar.append(i)
         
      for i in range(min(len(self_word_ar), len(other_word_ar)), max(len(self_word_ar), len(other_word_ar))):
         word_mismatch_ar.append(i)

      def_mismatch_ar = []   # will contain indexes of mismatching definition components
      self_def_ar = sorted([i.lower() for i in self.def_ar])
      other_def_ar = sorted([i.lower() for i in other.def_ar])

      for i in self_def_ar:
         if i not in other_def_ar:
            try:
               def_mismatch_ar.append(self.def_ar.index(i)) # will return index in unsorted ar
            except:
               pass

      return [word_mismatch_ar, def_mismatch_ar]
   
   def return_word(self):
      print(self.word_ar, self.def_ar)


def read_words_from_file(filepath:str) -> list:
   ar = []
   with open(filepath,"r") as f:
      data = f.readlines()
      newline_removed_data = [i.replace("\n","") for i in data]
      for line in newline_removed_data:
         ar.append(Latin_Word(line))
   return ar


def quiz_with_vocab_file(word_list:str) -> [int, int]:
   correct_question_num = 0
   
   if SETTINGS["ShuffleWords"]:
      random.shuffle(word_list)
      random.shuffle(word_list)
      random.shuffle(word_list)
   
   for cur_index in range(len(word_list)):
      word = word_list[cur_index]
      print("-----------------------------")
      print(f"WORD {cur_index + 1}: {word.word_ar[0]}")
      user_ans = input()
      
      # add option to cancel last submission
      if user_ans.lower().replace(" ","") == 'cancel':
         truncate_last_line(SETTINGS["MissedWordPath"])
         print("-----------------------------")
         print(f"WORD {cur_index + 1}: {word.word_ar[0]}")
         user_ans = input()

      user_ans_classobj = Latin_Word(user_ans)

      if user_ans_classobj == word:
         print("Correct!")
         correct_question_num += 1
      else:
         with open(SETTINGS["MissedWordPath"],"a") as f:
            f.write(str(word) + "\n")
         print("Incorrect!")
         correct_mismatches = word.return_mismatches(user_ans_classobj)
         incorrect_mismatches = user_ans_classobj.return_mismatches(word)

         print("Correct Answer:", word.to_str(colored_ar = correct_mismatches, color = "green"))
         print("Your Answer:", user_ans_classobj.to_str(colored_ar = incorrect_mismatches, color = "red"))

   return [correct_question_num, len(word_list)]


def ask_questions():
   while True:
      normal_missed = input("Normal or Missed words? ([n]/[m])\n")
      if normal_missed == "n":
         if SETTINGS["UseMostRecent"]:
            list_path = get_most_recent_edited_file()
         else:
            list_path = SETTINGS["DefaultVocabFilePath"]
         break
      elif normal_missed == "m":
         list_path = SETTINGS["MissedWordPath"]
         break
      else:
         print("NOT A VALID OPTION")
   
   print(f"Using word_list [{list_path}]...")
   word_list = read_words_from_file(list_path)
   with open(SETTINGS["MissedWordPath"],"w") as f:   pass  #clears missed_words file
   score = quiz_with_vocab_file(word_list)
   print(score[0], "/", score[1])



def get_most_recent_edited_file():
   basepath = "vocab_lists/"
   max = 0
   max_file_path = ""
   for cur_dir, subdirs, files in os.walk(basepath):
      for fname in files:
         full_path = os.path.join(cur_dir, fname)
         if os.path.getmtime(full_path) > max:
            max = os.path.getmtime(full_path)
            max_file_path = full_path
   return max_file_path


def truncate_last_line(file_path):
   with open(file_path, 'r') as f:
      lines = f.readlines()
      lines = lines[:-1]
   
   with open(file_path, 'w') as f:
      for i in lines:
         f.write(i)


def main():
   load_settings()

   while True:
      ask_questions()

main()

