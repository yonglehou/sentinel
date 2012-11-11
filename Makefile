.PHONY: all sentineld sentinel compile-thrift clean

THRIFT := /usr/local/bin/thrift

all: clean compile-thrift

setup:
	sudo python setup.py install

compile-thrift: sentinel.thrift
	@mkdir -p src/thrift
	@$(THRIFT) --gen py -out src/thrift $^
	@rm -rf src/sentinel/thrift
	@mv src/thrift/sentinel src/sentinel/thrift
	@rm -rf src/thrift

clean:
	@rm -rf build
	@rm -rf src/sentinel/*.pyc
	@rm -rf src/sentinel/thrift
