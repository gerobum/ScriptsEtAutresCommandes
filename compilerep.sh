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
rm *.aux *.log *.out *.snm *.toc *.nav *.vrb
