Summary:    MACS2
Name:       macs2
Version:    2.0.10
Release:    3
License:    GPL
Vendor:     DFCI
Group: Applications/Life Sciences
Source:     macs2-%{version}.zip
Packager:   TACC - wonaya@tacc.utexas.edu
BuildRoot:  /var/tmp/%{name}-%{version}-buildroot

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
%include ../rpm-dir.inc
%include ../system-defines.inc

# Compiler Family Definitions
# %include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs

%define PNAME macs2
%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_MACS2

%description
MACS2 empirically models the length of the sequenced ChIP fragments and uses it to improve the spatial resolution of predicted binding sites

## PREP
# Use -n <name> if source file different from <name>-<version>.zip
%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP
%setup -n MACS-master
%build
%install
%include ../system-load.inc
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load TACC
module swap intel gcc
module load python
python setup.py install --user
cp -r bin/* lib README.rst $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -r /home1/02114/wonaya/.local/lib/python2.7/site-packages/MACS2 $RPM_BUILD_ROOT/%{INSTALL_DIR}/lib/.
rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help (
[[
This module loads %{PNAME}.
To call this function, type %{PNAME} on the command line.
Documentation for %{PNAME} is available online at the publisher website: https://github.com/taoliu/MACS/
For convenience %{MODULE_VAR}_DIR points to the installation directory. 
PYTHONPATH has been prepended to include the MACS2 library.
Version %{version}
]])

whatis("Name: ${PNAME}")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, High-throughput Sequencing")
whatis("Description: MACS2 - Model-based Analysis of ChIP-Seq")
whatis("URL: https://github.com/taoliu/MACS")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}/")
prepend_path("PYTHONPATH"       ,"%{INSTALL_DIR}/lib/")
prepend_path("PATH"       ,"%{INSTALL_DIR}/")
<<<<<<< HEAD
=======

>>>>>>> ab5d67f58051e5a968300389af6ffb19acf82c8b
prereq("python")

EOF

#--------------
#  Version file.
#--------------
cat > $RPM_BUILD_ROOT%{MODULE_DIR}/.version.%{version} << 'EOF'
#%Module3.1.1#################################################
##
## version file for %{PNAME}-%{version}
##

set     ModulesVersion      "%{version}"
EOF

#------------------------------------------------
# FILES SECTION
#------------------------------------------------
%files

# Define files permisions, user and group
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

#------------------------------------------------
# CLEAN UP SECTION
#------------------------------------------------
%post
%clean
# Make sure we are not within one of the directories we try to delete
cd /tmp

# Remove the installation files now that the RPM has been generated
rm -rf $RPM_BUILD_ROOT

