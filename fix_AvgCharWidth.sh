#!/bin/sh
D=$1
for f in $D/*.ttf ;
do
    ttx -t 'OS/2' $f
    base=`basename $f .ttf`
    echo $D/$base.ttx
    sed -i -e 's/xAvgCharWidth value=".*"/xAvgCharWidth value="1024"/' $D/$base.ttx
    ttx -m $D/$base.ttf $D/$base.ttx
    rm -f $D/$base.ttx
    mv $D/$base\#1.ttf $f
done
