Summary: Memory-efficient short read (NGS) aligner
Name: bowtie
Version: 1.1.1
Release: 1
License: GPL
Group: Applications/Life Sciences
Source: %{name}-%{version}-src.zip
Packager: TACC - gzynda@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

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
%define APPS    /opt/apps
%define MODULES modulefiles
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}
%define PNAME %{name}
%define MODULE_VAR TACC_BOWTIE

# Compiler-specific packages
# %package -n %{name}-%{comp_fam_ver}
# Group: Applications/Life Sciences
# Summary: Memory-efficient short read (NGS) aligner

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
Bowtie is an ultrafast, memory-efficient short read aligner. It aligns short DNA sequences (reads) to the human genome at a rate of over 25 million 35-bp reads per hour. Bowtie indexes the genome with a Burrows-Wheeler index to keep its memory footprint small: typically about 2.2 GB for the human genome (2.9 GB for paired-end).

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep
[ -n "$RPM_BUILD_ROOT" -a "$RPM_BUILD_ROOT" != / ] && rm -rf ${RPM_BUILD_ROOT}
%setup -n %{name}-%{version}

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build
%include ../system-load.inc
module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc/4.7.1
make EXTRA_FLAGS="-Wl,-rpath,$GCC_LIB"

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp bowtie bowtie-build bowtie-build-[ls] bowtie-align-[ls] bowtie-inspect-[ls] $RPM_BUILD_ROOT/%{INSTALL_DIR}
cp -R scripts doc $RPM_BUILD_ROOT/%{INSTALL_DIR}


 
# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{PNAME}
distribution. Documentation can be found online at http://bowtie-bio.sourceforge.net/

This module provides the bowtie, bowtie-build, and bowtie-inspect binaries + associated scripts.

Version %{version}
]])

whatis("Name: Bowtie")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing")
whatis("URL: http://bowtie-bio.sourceforge.net/index.shtml")
whatis("Description: Ultrafast, memory-efficient short read aligner")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_SCRIPTS","%{INSTALL_DIR}/scripts")
prepend_path("PATH","%{INSTALL_DIR}")
prepend_path("PATH" ,"%{MODULE_VAR}_SCRIPTS")
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
#%files -n %{name}-%{comp_fam_ver}
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

