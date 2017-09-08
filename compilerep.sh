#!/bin/bash


for j in *fascicule*.tex *article*.tex *presentation*.tex  *portrait*.tex *paysage*.tex *note*.tex
do
    if [ -f "$j" ] 
    then
        pdflatex -halt-on-error "$j"
    fi
done
for j in *fascicule*.tex *article*.tex *presentation*.tex  *portrait*.tex *paysage*.tex *note*.tex
do
    if [ -f "$j" ] 
    then
        pdflatex -halt-on-error "$j"
    fi
done
rm *.fdb_latexmk *.fls *.tex~ *.backup *.aux *.log *.out *.snm *.toc *.nav *.vrb > /dev/null 2>&1
