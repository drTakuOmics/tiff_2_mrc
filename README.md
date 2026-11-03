# TIFF to MRC for CryoSPARC

Convert electron-microscopy TIFF images to MRC with IMOD, with an optional workaround for a reported TIFF metadata problem from the WVU EM scope.

**Start with normal IMOD conversion.** Use the metadata-cleaning script only when a warning has been traced to null bytes in `ImageDescription`. The script does not perform TIFF-to-MRC conversion.

## 1. Convert with IMOD

### Requirements

- [IMOD](https://bio3d.colorado.edu/imod/) with `tif2mrc` available in your terminal, or use its full executable path.
- Original TIFF files and a separate output directory.
- The correct acquisition pixel size for downstream processing.

Python and Pillow are only needed for the optional cleaner below. GPU/CUDA support is not required for this conversion command.

### Convert one file

```text
tif2mrc input.tif output.mrc
```

The same command accepts a `.tiff` input. For a multipage TIFF, IMOD can create an MRC stack; **do not pass that TIFF through this repository's cleaner**.

See the [official tif2mrc manual](https://bio3d.colorado.edu/imod/doc/man/tif2mrc.html) for supported image types and conversion options. Multiple input TIFFs in a single invocation are combined into one output stack. Use a loop when you want one MRC file per TIFF.

### Convert a directory on Windows

First prepare a directory containing **exactly one selected TIFF per image**: either its original or its validated cleaned copy. Do not mix both versions. Run one of the examples below from that directory. Use an empty `mrc` output directory for a new conversion run.

The output names retain the TIFF extension, for example `image.tif.mrc`, to avoid collisions between `image.tif` and `image.tiff`.

**Command Prompt (CMD), interactive terminal:**

```bat
mkdir mrc
for %f in (*.tif) do tif2mrc "%f" "mrc\%~nxf.mrc"
```

This example selects `.tif` files. For a directory of `.tiff` files, change the pattern to `*.tiff`. In a saved `.bat` file, replace both occurrences of `%f` / `%~nxf` with `%%f` / `%%~nxf`. Check each command's output for errors before importing the results.

**PowerShell, selecting both extensions:**

```powershell
$tif2mrc = "C:\YourPath\IMOD\bin\tif2mrc.exe"
New-Item -ItemType Directory -Path ".\mrc" -Force | Out-Null

Get-ChildItem -File |
    Where-Object { $_.Extension -in ".tif", ".tiff" } |
    Sort-Object Name |
    ForEach-Object {
        $output = Join-Path (Join-Path $PWD.Path "mrc") ($_.Name + ".mrc")
        & $tif2mrc $_.FullName $output
        if ($LASTEXITCODE -ne 0) {
            throw "tif2mrc failed for $($_.FullName)"
        }
    }
```

Replace the executable path with your IMOD installation path. If `tif2mrc` is already on your PATH, set `$tif2mrc = "tif2mrc"`.

### Output type and pixel size

Do not add conversion flags solely to suppress a warning. In particular, `-B 0` selects unsigned storage for byte output; it is **not** a metadata-cleaning option or a general instruction to convert every image to 8-bit.

Check output numeric type, intensity range and pixel spacing before downstream import. The conversion does not establish the correct microscope calibration automatically. Use the actual acquisition information when setting up CryoSPARC.

## 2. Why this repository includes a metadata cleaner

The original workflow reported warnings during IMOD conversion or CryoSPARC import associated with null bytes in TIFF `ImageDescription` metadata from the WVU EM scope.

`check_tiff_metadata.py` examines tag 270 (`ImageDescription`), looks for `\x00`, and attempts to save a copy after removing those characters.

This is a **targeted workaround for that reported metadata issue**, not a required preparation step for all microscopy TIFFs. The repository does not include an example problem TIFF, microscope/export-software version, exact warning text or a regression test demonstrating the diagnosis. A warning from a different source should be investigated before rewriting image files.

## 3. Optional workaround for single-frame TIFFs

> **Preserve the originals. Do not use the current cleaner on multipage TIFFs, movie frames stored in one TIFF, or other stacks.** It opens the initial image and saves without a multiframe preservation workflow, so additional pages may be lost.

### Prepare and run

1. Copy only the affected **single-frame** TIFFs into a new working directory. Keep the original files elsewhere. The current script selects lowercase `.tif` filenames only; `.tiff` and uppercase extensions are not selected.
2. Install Python and Pillow if needed:

   ```text
   python -m pip install Pillow
   ```

3. Download [check_tiff_metadata.py](check_tiff_metadata.py) and change its `directory` variable to your working directory:

   ```python
   directory = r"C:\Users\YourName\TIFF_working_copy"
   ```

4. Run the script:

   ```text
   python check_tiff_metadata.py
   ```

For a selected file with detected null bytes, the script attempts to write `cleaned_<original_filename>.tif` alongside the working copy. It does not create a cleaned file when no null byte is detected.

### Understand the current limitations

- The final list records files where null bytes were **detected**, not a verified list of successfully repaired outputs. A save can fail after a filename is added to that list.
- The script does not reopen the saved TIFF or compare pixels, metadata, image dimensions or frame count.
- Preservation of acquisition-specific TIFF tags is not guaranteed by this rewrite.
- Re-running it in the same directory can also scan existing `cleaned_` files or replace an existing cleaned output. Use a fresh working directory for each attempt.
- Selecting every TIFF in the working directory for conversion would include both originals and cleaned copies. After validation, copy only the chosen version of each image to the conversion directory described above.

## 4. Validate before processing

For a small representative subset first:

- Confirm the input is single-frame before cleaning.
- Reopen the cleaned TIFF and verify dimensions, frame count, numeric type and decoded pixel values against its original.
- Check that `ImageDescription` no longer contains the targeted null bytes, and inspect any acquisition metadata needed downstream.
- Convert the selected TIFF and check MRC dimensions, sections, numeric type, intensity range and pixel size. Account for any deliberately chosen conversion options.
- Inspect the image and test the intended CryoSPARC import. Record exact warnings and software versions.

A successful save, a printed summary or disappearance of one warning does not by itself establish that image data and metadata were preserved. Keep the originals until the outputs have been validated.

These checks are a validation checklist; the current Python script does not automate them. No end-to-end validation dataset or automated tests are included in this repository.

## References

- [IMOD tif2mrc manual](https://bio3d.colorado.edu/imod/doc/man/tif2mrc.html)
- [Pillow TIFF documentation](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#tiff)

## License

The code is freely available to download and run, but it’s protected and
licensed under a [Creative Commons Attribution-ShareAlike 4.0
International License](https://creativecommons.org/licenses/by-nc/4.0/),
meaning you can use it but citing it’s source.

[![License: CC BY-NC
4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
