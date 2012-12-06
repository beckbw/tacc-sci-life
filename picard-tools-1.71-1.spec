# $Id$

## Picard tools is Java and is distributed compiled
## http://downloads.sourceforge.net/project/picard/picard-tools/1.71/picard-tools-1.71.zip

Summary: Picard - Manipulate SAM files
Name: picard
Version: 1.71
Release: 1
License: MIT License
Vendor: Broad Institute
Group: Life Science Computing
Source0:  picard-tools-1.71.zip
Packager: TACC - vaughn@tacc.utexas.edu
BuildRoot: /var/tmp/%{name}_%{version}-buildroot

%define debug_package %{nil}
%include rpm-dir.inc

%define PNAME picard
%define APPS /opt/apps
%define MODULES modulefiles

%define INSTALL_DIR %{APPS}/%{PNAME}/%{version}
%define MODULE_DIR  %{APPS}/%{MODULES}/%{PNAME}
%define MODULE_VAR TACC_PICARD

%description
Picard comprises Java-based command-line utilities that manipulate SAM files, and a Java API (SAM-JDK) for creating new programs that read and write SAM files. Both SAM text format and SAM binary (BAM) format are supported.

%prep
rm   -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n picard-tools-1.71

%build

if [ -f "$BASH_ENV" ]; then
  export MODULEPATH=/opt/apps/modulefiles:/opt/modulefiles
  . $BASH_ENV
fi


module purge
module load TACC

echo "Picard-tools is distributed as compiled Java. No compilation necessary."

%install
mkdir -p $RPM_BUILD_ROOT%{INSTALL_DIR}
cp -R ./* $RPM_BUILD_ROOT/%{INSTALL_DIR}

#-----------------
# Modules Section
#-----------------

rm -rf $RPM_BUILD_ROOT%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT%{MODULE_DIR}
cat   >  $RPM_BUILD_ROOT%{MODULE_DIR}/%{version}.lua << 'EOF'
help(
[[
The %{PNAME} module file defines the following environment variables:
%{MODULE_VAR}_DIR for the location of the %{PNAME} distribution.

Invoke as follows:

java jvm-args -jar $%{MODULE_VAR}_DIR/<PicardCommand.jar> [opts]

Version %{version}
]]
)

whatis("Name: Picard")
whatis("Version: %{version}")
whatis("Category: computational biology, genomics")
whatis("Keywords:  Biology, Genomics, Quality Control, Utility, Sequencing")
whatis("URL: http://picard.sourceforge.net/")
whatis("Description: Picard comprises Java-based command-line utilities that manipulate SAM files, and a Java API (SAM-JDK) for creating new programs that read and write SAM files. Both SAM text format and SAM binary (BAM) format are supported.")

setenv (     "%{MODULE_VAR}_DIR", "%{INSTALL_DIR}/")

prereq ("jdk64")

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

%files
%defattr(755,root,root,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%clean
rm -rf $RPM_BUILD_ROOT

