# Macros On Save

A minimal python script you can use anywhere to perform substitutions of your specifications on save.

https://github.com/StanleyNeoh/macrosOnSave/assets/95394480/9a6bb129-f139-4b8a-96ed-6b7b9d38d9db

## Setup and installation

1. `git clone` / `git submodule` this repository into the project folder
2. Ensure you have python3 installed
3. While at the root of your project folder, run the following command.
```
python macroOnSave/main.py
```
4. If this is your first time, a `macro_config.json` file would be created.
5. Edit the `macro_config.json` file to your requirement.
   1. `watch_dir` is the directory which macros will be enabled.
   2. `macro_dir` is the directory where you define your macros.
6. Re-run `python macrosOnSave/main.py` to start the program.

## Usage

Suppose you set your `watch_dir` as `src/` and `macro_dir` as `macro/`.

And you are working on a file `src/A/main.cpp` which has the following content.
```cpp
// src/A/main.cpp
#include <iostream>

int main() {
    std::cout << "Hello World\n";
}
```

And you have defined a macro in `macro/B/bye.cpp`. Note that only the lines between `...MACRO-START...` and `...MACRO-END...` will be used.

```cpp
// macro/B/bye.cpp - Start
#include <iostream>

// MACRO-START
void bye() {
    std::cout << "Goodbye\n";
}
// MACRO-END
```

Then simply by typing `>>> <substring of macro file name>` like `>>> by` or `>>> bye.c`,
```cpp
// src/A/main.cpp
#include <iostream>

>>> by

int main() {
    std::cout << "Hello World\n";
}
```

Turns into the following on save

```cpp
// src/A/main.cpp
#include <iostream>

void bye() {
    std::cout << "Goodbye\n";
}

int main() {
    std::cout << "Hello World\n";
}
```

Its just that simple.

## Notes
1) Macros are line level replacements. So expect the line containing `>>> <filename>` to be replaced with the file contents of the macro.
2) You can define macros in subdirectories, of `macro_dir` as the program will scour the directory for a suitable file.
