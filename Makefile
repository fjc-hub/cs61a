.PHONY: test clean

test:
	python3 ok --local

clean:
	rm -rf .ok_*