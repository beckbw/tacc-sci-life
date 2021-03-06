# $Id$

Name: bowtie
Version: 2.0.0b7
Release: 1
License: GPL
Group: Applications/Life Sciences
Source:  bowtie2-2.0.0-beta7-source.zip
Packager: TACC - vaughn@tacc.utexas.edu
Summary: Memory-efficient short read (NGS) aligner

#------------------------------------------------
# BASIC DEFINITIONS
#------------------------------------------------
# %define debug-package %{nil}
# This will define the correct _topdir
%include rpm-dir.inc
# Compiler Family Definitions
%include compiler-defines.inc
# MPI Family Definitions
# %include mpi-defines.inc
# Other defs
%define system linux
%define APPS    /opt/apps
%define MODULES modulefiles
%define PNAME %{name}

#%package -n %{name}-%{comp_fam_ver}
#Group: Applications/Life Sciences
#Summary: Memory-efficient short read (NGS) aligner

#------------------------------------------------
# PACKAGE DESCRIPTION
#------------------------------------------------
%description
#%description -n %{name}-%{comp_fam_ver}
Bowtie 2 is an ultrafast and memory-efficient tool for aligning sequencing reads to long reference sequences. It is particularly good at aligning reads of about 50 up to 100s or 1,000s of characters, and particularly good at aligning to relatively long (e.g. mammalian) genomes. Bowtie 2 indexes the genome with an FM Index to keep its memory footprint small: for the human genome, its memory footprint is typically around 3.2 GB. Bowtie 2 supports gapped, local, and paired-end alignment modes.

#------------------------------------------------
# INSTALLATION DIRECTORY
#------------------------------------------------
# Buildroot: defaults to null if not included here
# Buildroot: defaults to null if not included here
#%define INSTALL_DIR %{APPS}/%{comp_fam_ver}/%{name}/%{version}
#%define MODULE_DIR  %{APPS}/%{comp_fam_ver}/%{MODULES}/%{name}
%define INSTALL_DIR %{APPS}/%{name}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{name}

%define MODULE_VAR TACC_BOWTIE

#------------------------------------------------
# PREPARATION SECTION
#------------------------------------------------
# Use -n <name> if source file different from <name>-<version>.tar.gz
%prep

# Remove older attempts
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

# Unpack source
# This will unpack the source to /tmp/BUILD/*
%setup -n bowtie2-2.0.0-beta7

#------------------------------------------------
# BUILD SECTION
#------------------------------------------------
%build

# Start with a clean environment
if [ -f "$BASH_ENV" ]; then
   . $BASH_ENV
   export MODULEPATH=/opt/apps/teragrid/modulefiles:/opt/apps/modulefiles:/opt/modulefiles
fi

module purge
module load TACC
module swap $TACC_FAMILY_COMPILER gcc/4.4.5

# Since LDFLAGS is not used in compilation, we hijack EXTRA_FLAGS to carry the rpath payload
make EXTRA_FLAGS="-Wl,-rpath,/opt/apps/gcc/4.4.5/lib64/"

#------------------------------------------------
# INSTALL SECTION
#------------------------------------------------
%install
cp -R ./bowtie2 ./bowtie2-align ./bowtie2-build ./bowtie2-inspect ./doc ./scripts $RPM_BUILD_ROOT/%{INSTALL_DIR}

# ADD ALL MODULE STUFF HERE
# TACC module

rm   -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help (
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR and %{MODULE_VAR}_SCRIPTS for the location of the %{PNAME}
distribution. Documentation can be found online at http://bowtie-bio.sourceforge.net/bowtie2/

NOTE: Bowtie2 indexes are not backwards compatible with Bowtie1 indexes. 

This module provides the bowtie2, bowtie2-align, bowtie2-build, and bowtie2-inspect binaries + scripts

Version %{version}

]])

whatis("Name: Bowtie")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords: Biology, Genomics, Alignment, Sequencing")
whatis("URL: http://bowtie-bio.sourceforge.net/bowtie2/")
whatis("Description: Ultrafast, memory-efficient short read aligner")

setenv("%{MODULE_VAR}_DIR","%{INSTALL_DIR}")
setenv("%{MODULE_VAR}_SCRIPTS","%{INSTALL_DIR}/scripts")
prepend_path("PATH"       ,"%{INSTALL_DIR}")

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

