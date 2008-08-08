
%define name	projectx
%define Name	ProjectX
%define version	0.90.4.00.b24
%define shortv	0.90.4
%define gcj_support 1
%if %mdkversion >= 200810
# (Anssi 02/2008) gcj4.3 segfault
%define gcj_support 0
%endif
%define stable	0

Summary:	ProjectX - a free Java based demux utility
Name:		%name
Version:	%version
Release:	%mkrel 4
License:	GPL
URL:		http://project-x.sourceforge.net/
%if %stable
Source:		%{Name}_Source_eng_%{version}.tar.bz2
Source1:	%{Name}_LanguagePack_%{version}.zip
%else
Source:		%{name}-%{version}.tar.bz2
%endif
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-buildroot
Requires:	java
Requires:	jpackage-utils
Requires:	jakarta-commons-net
Requires:	jakarta-oro
BuildRequires:	java-devel
%if %{mdkversion} >= 200810
BuildRequires:	java-rpmbuild
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	jakarta-commons-net
BuildRequires:	jakarta-oro
BuildRequires:	ImageMagick
BuildRequires:	dos2unix
BuildRequires:  desktop-file-utils
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
Converts, splits and demuxes DVB and other MPEG recordings.

%prep
%if %stable
%setup -q -n %{Name}_Source_%{shortv} -b 1
%else
%setup -q -n Project-X
%endif
rm -rf lib
find -name CVS -type d -print0 | xargs -0 rm -rf
dos2unix htmls/*.html htmls/*/*.html

perl -pi -e 's,classpath [a-z0-9\.\/:-]*,classpath \$CLASSPATH,' build.sh
perl -pi -e 's,^javac ,%javac ,' build.sh

%if %mdkversion <= 200800
# We call jar manually to workaround
# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=32516
perl -pi -e 's,^jar ,#jar ,' build.sh
%else
perl -pi -e 's,^jar ,%jar ,' build.sh
%endif

perl -pi -e 's,^Class-Path:.*\n,,' MANIFEST.MF

perl -pi -e 's,Icon=.*,Icon=%name,' %name.desktop
perl -pi -e 's,Exec=.*,Exec=%{_bindir}/%{name},' %name.desktop

perl -pi -e 's/\r$//g' *.txt

%build
export CLASSPATH=$(build-classpath commons-net oro)
sh -ex build.sh

%if %mdkversion <= 200800
cd build
%jar cfvm ../ProjectX.jar ../MANIFEST.MF *
cd -
%endif

%jar -i %Name.jar

%install
rm -rf %{buildroot}

install -d -m755 %{buildroot}%{_javadir}
install -m644 %{Name}.jar %{buildroot}%{_javadir}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%jpackage_script net.sourceforge.dvb.projectx.common.Start %nil %nil %Name:commons-net:oro %name

install -D -m644 %name.desktop %{buildroot}%{_datadir}/applications/%name.desktop

install -d -m755 %{buildroot}%{_miconsdir}
install -d -m755 %{buildroot}%{_iconsdir}
install -d -m755 %{buildroot}%{_liconsdir}

# (Anssi) It is X :p
convert resources/close.gif -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert resources/close.gif -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert resources/close.gif -resize 48x48 %{buildroot}%{_liconsdir}/%{name}.png


desktop-file-install --vendor="" \
  --add-category="Java" \
  --add-category="AudioVideo" \
  --add-category="AudioVideoEditing" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%clean
rm -rf %{buildroot}

%post
%if %{gcj_support}
%{update_gcjdb}
%endif
%if %mdkversion < 200900
%{update_menus}
%endif

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif
%if %mdkversion < 200900
%{clean_menus}
%endif

%files
%defattr(0644,root,root,0755)
%doc ReadMe.txt htmls zutun.txt
%attr(0755,root,root) %{_bindir}/%{name}
%{_javadir}/%{Name}.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/%{name}.desktop



