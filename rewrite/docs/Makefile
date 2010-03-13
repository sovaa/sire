all:
	echo -e '#!/usr/bin/python\n\nimport sys\nif len(sys.argv) < 2:\n    sys.exit()\nif sys.argv[1] == "--version":\n    print """\n' > sireman
	sire --version >> sireman
	echo -e '"""\n\n' >> sireman
	echo -e 'elif sys.argv[1] == "--help":\n    print """\n' >> sireman
	sire --help >> sireman
	echo -e '"""\n\n' >> sireman
	chmod +x sireman
	#mv sireman /usr/local/bin/
	help2man --include ../README ./sireman > sire.1
	bzip2 sire.1
	rm sireman
	#mv sire.1.bz2 /usr/local/share/man/man1/
