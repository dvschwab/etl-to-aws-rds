# Unit Tests for extract-fields()

* The function should return the correct field from CSV, pipe, and semi-colon delimited files
* The function should error when the position argument is not an integer, or is negative
* The function should return only unique values when the field contains duplicate values
* The function should handle common file-handling errors
* The function should sort the field when the --sorted parameter is True
* The function should error when given incorrect arguments
	* Missing input, output, or position
	* Incorrect delimiter
	* Unspecified arguments
* The function should use the comma delimiter if the delimiter is unspecified
* The function should display help text when the --help argument is passed
* The function should error when the field position is greater than the number of fields
