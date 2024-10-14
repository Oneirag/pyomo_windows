# Downloading solvers

For all the following instructions, leave the files in any folder and pass that folder as parameter `executable` to the `SolverFactory` method of `pyomo`. 


## GLPK
Download binaries from http://sourceforge.net/projects/winglpk/. From the download folder, just `glpsol.exe` and `glpk_4_65.dll` are needed from the `w64` folder. 


## IPOPT
Download binaries from https://github.com/coin-or/Ipopt/releases. Get `md` version **(not mdd)** and copy full bin folder of zip


## HIGHS
Needs to be installed from source. Start by cloning repository with `git clone https://github.com/ERGO-Code/HiGHS.git
`, then

Path for visual studio build tools: `C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC\14.29.30133\bin\Hostx64\x64`

````commandline
cd HiGHS
mkdir build
cd build
cmake -DFAST_BUILD=ON ..
cmake --build .
````

## COIN-CBC
Download binaries from https://github.com/coin-or/Cbc/releases, get binary `https://github.com/coin-or/Cbc/releases/download/releases%2F2.10.12/Cbc-releases.2.10.12-windows-2022-msvs-v17-Release-x64.zip`
Copy `cbc.exe` to the cbc folder in solvers 

