all:
	#cat ../README | sed "s/\(.*\)/\1\n/g" > README.temp
	#help2man --include ./README.temp sire > sire.1
	help2man --include ../README sire > sire.1
	bzip2 sire.1
	#rm README.temp
	#mv sire.1.bz2 /usr/local/share/man/man1/

clean:
	rm sire.1.bz2
	rm /usr/local/man/man1/sire.1.bz2
