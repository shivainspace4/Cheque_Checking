Algorithm:

Input is PDF:
Change PDF to Image
	1. # Check if the image data is compressed using a filter
	2. Check if the Filter type is correct
	3. Convert single filter to list type
	4. Handle different filter types (e.g., /FlateDecode)

Wrap Image Data:
	1. Use io.BytesIO to wrap the image data before passing it to Image.open()
	2. Convert the image to the desired mode (if different from original mode)
	3. Resize the image if needed (using img.resize, if necessary)

Extract Text from Image with OCR
	1. Check if Date is predated
		1. Extract Date from Text
		2. Check the converted string to the date current date
		3. Convert matched string to date object, assuming pattern like 'DD-MM-YYYY'
                4. If the date format is different, you might need to handle it here

	2. Compare Numeric and Written Amount:
		1. Extract both written and numeric text from image
		2. Convert numeric string to float
		3. Convert written amount to numeric
	
	3. Check signature
		1. To use image comparison algorithms and ML models for signature verifications

