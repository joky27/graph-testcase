#!/bin/bash
#generate seed files
g++ lemon_dij_test.cpp -o lemon -lemon -ftest-coverage -fprofile-arcs

function MakeDir()
{
if [ ! -d "$1" ];then
    mkdir $1    
fi
}

function GetSeedCov()
{
covpath='cov'
MakeDir $covpath
filepath="seed"
files=$(ls $filepath)   
for file in $files
do 
    #echo ${file%.*} 
    ./lemon $filepath"/"${file} 
    lcov -d . -c  -o  ${file%.*}".info" 
    genhtml -o "cov/"${file%.*}  ${file%.*}".info" 
    grep "headerCovTableEntry"<"cov/"${file%.*}"/usr/local/include/lemon/index.html">"cov/"${file%.*}".txt"
    lcov -d . --zerocounter
    rm -rf "cov/"${file%.*}
    rm -rf ${file%.*}".info" 
done 
}

function GetCombine()
{
filepath="seed"
files=$(ls $filepath)   
for file in $files
do 
    #echo ${file%.*} 
    ./lemon $filepath"/"${file}    
done 
lcov -d . -c  -o  "seed.info" 
genhtml -o "combine"  "seed.info" 
grep "headerCovTableEntry"<"combine/usr/local/include/lemon/index.html">"seed.txt"
lcov -d . --zerocounter
rm -rf "combine"
}

function GetCov()
{
echo "round: $index"
path="modify/"$index
filename=$(ls $path)
infopath="info"
mkdir $infopath
./lemon $path"/"${filename} 
lcov -d . -c  -o "info/"$index".info"
genhtml  -o "cov/${filename%.*}"  "info/"$index".info" #info records the 
grep "headerCovTableEntry"<"cov/"${filename%.*}"/usr/local/include/lemon/index.html">"cov/"${filename%.*}".txt"
lcov -d . --zerocounter
rm -rf "cov/${filename%.*}"
genhtml -o "cov/combine" "info/"$index".info" "seed.info"
grep "headerCovTableEntry"<"cov/combine/usr/local/include/lemon/index.html">"cov/combine.txt"
rm -rf "cov/combine"
}

#zero=0
#for index in {0..10000}
#do 
#    if [ $index -eq $zero ]
#        then
#            python seed.py seed 1
#            GetSeedCov 
#            GetCombine
#            python seed.py seed 2          
#        else
#            python modify.py $index
#            GetCov
#            python select.py $index
#    fi
#done 
#GetSeedCov 
#GetCombine
index=1
GetCov