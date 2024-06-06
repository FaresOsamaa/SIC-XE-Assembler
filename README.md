
# SIC/SICXE Assembler

## Description

This Python script processes an assembly language program by reading an input file, generating intermediate and output files, and producing an HTE (Header, Text, End) record format. The script handles the location counter, opcode processing, and symbol table generation.

## Files

- `in.txt`: Input file containing the assembly language program.
- `intermediate.txt`: Intermediate file generated during processing.
- `out_pass1.txt`: Output file from the first pass of processing.
- `out_pass2.txt`: Output file from the second pass of processing.
- `symbTable.txt`: Symbol table file.
- `HTE.txt`: Final output file in HTE record format.

## Script Explanation

1. **Import Libraries**:
   - The script imports the `operator` module.

2. **File Handling**:
   - Opens the input file `in.txt` for reading.
   - Opens a new file `intermediate.txt` for writing.

3. **Process Input File**:
   - Reads each line from `in.txt` and writes a substring to `intermediate.txt`.

4. **Initialize Opcode Tables**:
   - Defines opcode tables for different instruction sets.

5. **Open Intermediate and Output Files**:
   - Opens `intermediate.txt` for reading.
   - Opens various output files for writing.

6. **First Pass Processing**:
   - Writes the initial line to output files.
   - Extracts the program name and start address.
   - Processes each line in `intermediate.txt` to update the location counter and write to output files.

7. **Close Output Files**:
   - Closes the files `out_pass1.txt`, `out_pass2.txt`, and `symbTable.txt`.

8. **Second Pass Processing**:
   - Reads the processed file and generates the HTE record format.
   - Handles opcode processing and symbol table lookups.

9. **Write End Record**:
   - Writes the end record to `HTE.txt` and closes the file.

## How to Use

1. Place your assembly language program in the `in.txt` file.
2. Run the Python script.
3. The script will generate the following output files:
   - `intermediate.txt`: Intermediate file with processed lines.
   - `out_pass1.txt`: First pass output with location counters.
   - `out_pass2.txt`: Second pass output with opcodes and operands.
   - `symbTable.txt`: Symbol table with labels and addresses.
   - `HTE.txt`: Final output in HTE record format.


Run the script, and it will generate the corresponding output files.

## Notes

- Ensure that the input file `in.txt` follows the expected format for the assembly language program.
- The script assumes certain conventions for opcode and instruction formats.
