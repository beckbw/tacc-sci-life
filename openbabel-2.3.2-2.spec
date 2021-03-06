Name:     openbabel
Version:  2.3.2
Release:  2
License:  GNU General Public License
Source:   openbabel-2.3.2.tar.gz
URL:      http://openbabel.org/wiki/Main_Page
Packager: TACC - wallen@tacc.utexas.edu
Summary:  Chemical toolbox designed to speak the many languages of chemical data

#------------------------------------------------
# INITIAL DEFINITIONS
#------------------------------------------------

## System Definitions
%include ./include/system-defines.inc
%include ./include/%{PLATFORM}/rpm-dir.inc

## Compiler Family Definitions
# %include ./include/%{PLATFORM}/compiler-defines.inc
## MPI Family Definitions
# %include ./include/%{PLATFORM}/mpi-defines.inc
## directory and name definitions for relocatable RPMs
%include ./include/name-defines.inc

%define MODULE_VAR  %{MODULE_VAR_PREFIX}OPENBABEL
%define PNAME       openbabel

%package %{PACKAGE}
Summary:  Chemical toolbox designed to speak the many languages of chemical data
Group: Applications/Life Sciences
%description package

%package %{MODULEFILE}
Summary:  Chemical toolbox designed to speak the many languages of chemical data
Group: Applications/Life Sciences
%description modulefile

## PACKAGE DESCRIPTION
%description
Open Babel is a chemical toolbox designed to speak the many languages of chemical data. It's an open, collaborative project allowing anyone to search, convert, analyze, or store data from molecular modeling, chemistry, solid-state materials, biochemistry, or related areas. 


## PREP
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
%if %{?BUILD_PACKAGE}
    rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
%endif

%if %{?BUILD_MODULEFILE}
    rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
%endif

## SETUP
# Run the setup macro - this removes old copies, then unpackages the program zip file
# from ~SOURCES into ~BUILD
%setup -n %{PNAME}-%{version}

## BUILD
%build

#------------------------------------------------
# INSTALL 
#------------------------------------------------
%install

# Start with a clean environment
%include ./include/%{PLATFORM}/system-load.inc

#--------------------------------------
%if %{?BUILD_PACKAGE}
    mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{INSTALL_DIR}/.tacc_install_canary
    ########### Do Not Remove #############

    ## Install Steps Start
    module purge
    module load TACC

    %if "%{PLATFORM}" == "stampede"
        module swap $TACC_FAMILY_COMPILER gcc/4.4.6   # newer versions of gcc cause test failures
        module load cmake/3.1.0
        export CC=`which gcc`
        export CXX=`which g++`
    %endif

    %if "%{PLATFORM}" == "wrangler"
        # there are no gcc or cmake modules on wrangler currently
        # /usr/bin/gcc and /usr/bin/g++ are v4.4.7
        # /usr/bin/cmake is v2.8.12.2
        export CC=`which gcc`
        export CXX=`which g++`
    %endif

    # The objective of this section is to install the compiled software into a virtual
    # directory structure so that it can be packaged up into an RPM
    #
    # install is also a macro that does many things, including creating appropriate
    # directories in $RPM_BUILD_ROOT and cd to the right place

    # Install serial version
    cd $RPM_BUILD_DIR
    mv %{PNAME}-%{version} %{PNAME}-%{version}-cmake
    mkdir %{PNAME}-%{version}
    mkdir %{PNAME}-%{version}-cmake/build/
    cd %{PNAME}-%{version}-cmake/build/
    cmake -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_DIR/%{PNAME}-%{version} -Wno-dev ../
    make -j 2
    make install
    #make DESTDIR=$RPM_BUILD_ROOT install 


    # Copy the relevant files
    cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}/bin/     $RPM_BUILD_ROOT/%{INSTALL_DIR}/
    cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}/include/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
    cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}/lib/     $RPM_BUILD_ROOT/%{INSTALL_DIR}/
    cp -r $RPM_BUILD_DIR/%{PNAME}-%{version}/share/   $RPM_BUILD_ROOT/%{INSTALL_DIR}/
    #cp -r ../install/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/
%endif


#------------------------------------------------
# MODULEFILE CREATION
#------------------------------------------------
# Clean up the old module directory
#rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}

%if %{?BUILD_MODULEFILE}
    mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
    ##### Create TACC Canary Files ########
    touch $RPM_BUILD_ROOT/%{MODULE_DIR}/.tacc_module_canary
    ########### Do Not Remove #############


#--------------------------------------
## Modulefile Start
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
This module loads %{name} built with cmake and gcc.
Documentation for %{name} is available online at: http://openbabel.org/wiki/Main_Page/

The binary executables can be found in %{MODULE_VAR}_BIN
The include files can be found in %{MODULE_VAR}_INCLUDE
The library files can be found in %{MODULE_VAR}_LIB
The share files can be found in %{MODULE_VAR}_SHARE

Version %{version}

]])

whatis("Name: %{PNAME}")
whatis("Version: %{version}")
whatis("Category: computational chemistry, simulation")
whatis("Keywords: Biology, Chemistry, Molecular modeling, Format conversion")
whatis("Description: Open Babel is a chemical toolbox designed to speak the many languages of chemical data ")
whatis("URL: http://openbabel.org/wiki/Main_Page")

prepend_path("PATH",                  "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_DIR",     "%{INSTALL_DIR}")
setenv (     "%{MODULE_VAR}_BIN",     "%{INSTALL_DIR}/bin")
setenv (     "%{MODULE_VAR}_INCLUDE", "%{INSTALL_DIR}/include")
setenv (     "%{MODULE_VAR}_LIB",     "%{INSTALL_DIR}/lib")
setenv (     "%{MODULE_VAR}_SHARE",   "%{INSTALL_DIR}/share")

EOF
## Modulefile End
#--------------------------------------


    # Lua sytax check
    if [ -f $SPEC_DIR/checkModuleSyntax ]; then
        $SPEC_DIR/checkModuleSyntax $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua
    fi


#--------------------------------------
## VERSION FILE
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF
## VERSION FILE END
#--------------------------------------


%endif


#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%if %{?BUILD_PACKAGE}
%files %{PACKAGE}
%defattr(-,root,install,)
%{INSTALL_DIR}
%endif # ?BUILD_PACKAGE

%if %{?BUILD_MODULEFILE}
%files %{MODULEFILE}
%defattr(-,root,install,)
%{MODULE_DIR}
%endif # ?BUILD_MODULEFILE

## POST 
%post %{PACKAGE}
export PACKAGE_POST=1
%include include/post-defines.inc
%post %{MODULEFILE}
export MODULEFILE_POST=1
%include include/post-defines.inc

## CLEAN UP
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

