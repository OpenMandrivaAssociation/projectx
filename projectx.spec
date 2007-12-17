
%define name	projectx
%define Name	ProjectX
%define version	0.90.4.00
%define shortv	0.90.4
%define gcj_support 1

Summary:	ProjectX - a free Java based demux utility
Name:		%name
Version:	%version
Release:	%mkrel 8
License:	GPL
URL:		http://sourceforge.net/projects/project-x
Source:		%{Name}_Source_eng_%{version}.tar.bz2
Source1:	%{Name}_LanguagePack_%{version}.zip
Group:		Video
Requires:	java
Requires:	jpackage-utils
Requires:	jakarta-commons-net
Requires:	jakarta-oro
BuildRequires:	java-devel
BuildRequires:	java-rpmbuild
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
%setup -q -n %{Name}_Source_%{shortv} -b 1
dos2unix htmls/*.html htmls/*/*.html

perl -pi -e 's,classpath [a-z0-9\.\/:-]*,classpath \$CLASSPATH,' build.sh
perl -pi -e 's,^javac ,%javac ,' build.sh
# We call jar manually to workaround
# http://gcc.gnu.org/bugzilla/show_bug.cgi?id=32516
perl -pi -e 's,^jar ,#jar ,' build.sh

perl -pi -e 's,^Class-Path:.*\n,,' MANIFEST.MF

perl -pi -e 's,Icon=.*,Icon=%name,' %name.desktop
perl -pi -e 's,Exec=.*,Exec=%{_bindir}/%{name},' %name.desktop

perl -pi -e 's/\r$//g' *.txt

%build
export CLASSPATH=$(build-classpath commons-net oro)
sh -ex build.sh

cd build
%jar cfvm ../ProjectX.jar ../MANIFEST.MF *
cd -

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

convert resources/x.gif -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png
convert resources/x.gif -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert resources/x.gif -resize 48x48 %{buildroot}%{_liconsdir}/%{name}.png

install -d -m755 %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} << EOF
?package(%name): \
	needs="x11" \
	title="%{Name}" \
	longtitle="A video editing and demultiplexing tool" \
	icon="%{name}.png" \
	command="%{_bindir}/%{name}" \
	xdg="true" \
	section="Multimedia/Video"
EOF

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
%{update_menus}

%postun
%if %{gcj_support}
%{clean_gcjdb}
%endif
%{clean_menus}

%files
%defattr(0644,root,root,0755)
%doc ReleaseNotes* ReadMe.txt htmls
%attr(0755,root,root) %{_bindir}/%{name}
%{_javadir}/%{Name}.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_menudir}/%{name}
%{_datadir}/applications/%{name}.desktop



