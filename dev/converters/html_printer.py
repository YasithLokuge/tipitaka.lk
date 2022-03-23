import json
import os
import argparse
from pathlib import Path
from natsort import os_sorted
from domonic.html import *
import pypandoc

default_input_root_folder = str(Path("public").joinpath("static").joinpath("text"))
default_output_folder = Path("dev").joinpath("converters").joinpath("output")
default_output_file = str(default_output_folder.joinpath("tipitaka.html"))

data = {}

def files_in_dir(path, format, exclude_files):
  for entry in os_sorted(os.scandir(path)):
    if not entry.name.startswith('.') and entry.is_file() and entry.name.endswith(format) and entry.name not in exclude_files:
      yield entry.path

def scan(input_root_folder, output_file):
  print('Scanning ' + input_root_folder)
  index_file()
  for filename in files_in_dir(input_root_folder, 'json', exclude_files=[]):
    process(filename, output_file)

def change_ext(filename, from_format, to_format):
   return filename.replace(from_format, to_format)

def index_file():
  index_file = str(default_output_folder.joinpath('index.html'))
  with open(index_file, 'a+') as output:
    output.write(f"{html(head(title(metadata())), body())}")

def process(input_file, output_file):
  filename = os.path.basename(input_file)
  output_file = str(Path("dev").joinpath("converters").joinpath("output").joinpath(change_ext(filename, 'json', 'html')))

  print('Processing ' + input_file)
  with open(input_file, 'r') as input:
    data = json.load(input)

  with open(output_file, 'a+') as output:
    elements = []
    for page in data['pages']:
      for entry in page['sinh']['entries']:
        elements.append(type(entry))
    mydom = body(*elements)
    output.write(f"{mydom}")
  pypandoc.convert_file(
    output_file, 
    'epub', 
    outputfile=str(change_ext(output_file, 'html', 'epub')),
  )  

def metadata():
  return 'බුද්ධ ජයන්ති තිපිටක ග්‍රන්ථ සිංහල පරිවර්තනය'

def type(entry, style='text-align: justify;'):
  style = 'text-align: center;' if entry['type'] == 'centered' else style
  if 'level' not in entry:
    return p(entry['text'], _style=style)
  elif entry['level'] == 1:
    return h1(entry['text'], _style=style)
  elif entry['level'] == 2:
    return h2(entry['text'], _style=style)
  elif entry['level'] == 3:
    return h3(entry['text'], _style=style)
  elif entry['level'] == 4:
    return h4(entry['text'], _style=style)
  elif entry['level'] == 5:
    return h5(entry['text'], _style=style)
  else:
    return p(entry['text'], _style=style)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description = 'JSON to HTML converter')
  parser.add_argument('-i', '--input_root_folder', default=default_input_root_folder, help='input root folder default: public/static/text')
  parser.add_argument('-o', '--output_file', default=default_output_file, help='output html file name to be saved inside dev/converters/output folder')
  args = parser.parse_args()
  scan(args.input_root_folder, args.output_file)