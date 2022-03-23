#! /bin/bash

# Ex: ./dev/converters/convert.sh dev/converters/output tipitaka.epub epub 
root_dir=${1}
output_file=${2}
output_format=${3}
filter=${4}
echo "Converting $root_dir -> $output_file"
# find files with the given extension and sort them by number in the filename
# Pipe to `tr`` for arranging them in space seperated string
files=$(find $root_dir -maxdepth 1 -iname "*.html" -type f | sort --version-sort --field-separator=- | tr '\n' ' ')
# for some reason the last file comes to the top when converting to epub. So we are adding 'index.html' to the end of the list
if [[ $files =~ "index.html" ]]; then
    files="$files $root_dir/index.html"
fi
pandoc -f html -t ${output_format} -s ${files} -o dev/converters/output/$output_file --toc
