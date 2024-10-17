%define Name	ProjectX
%define shortv	0.91.0
%define gcj_support 1
%if %mdkversion >= 200810
# (Anssi 02/2008) gcj4.3 segfault
%define gcj_support 0
%endif
%define stable	0

Summary:	A free Java based MPEG demux utility
Name:		projectx
Version:	0.91.0
Release:	5
License:	GPLv2+
URL:		https://project-x.sourceforge.net/
%if %stable
Source:		%{Name}_Source_eng_%{version}.tar.bz2
Source1:	%{Name}_LanguagePack_%{version}.zip
%else
# Every CVS push (usually) corresponds to a .bXX tag.
# Latest tag can be seen in the commit message and in
# http://project-x.sourceforge.net/update/update.txt
# cvs -d:pserver:anonymous@project-x.cvs.sourceforge.net:/cvsroot/project-x login 
# cvs -z3 -d:pserver:anonymous@project-x.cvs.sourceforge.net:/cvsroot/project-x co -P project-x
Source:		%{name}-%{version}.zip
%endif
Group:		Video
Requires:	java >= 1.6
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
BuildRequires:	imagemagick
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
%setup -q -n Project-X_%{shortv}
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

%if %{gcj_support}
%post
%{update_gcjdb}
%endif

%if %{gcj_support}
%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc ReadMe.txt htmls
%attr(0755,root,root) %{_bindir}/%{name}
%{_javadir}/%{Name}.jar
%if %{gcj_support}
%{_libdir}/gcj/%{name}
%endif
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/%{name}.desktop





%changelog
* Sat Apr 30 2011 Olivier Faurax <ofaurax@mandriva.org> 0.91.0-1mdv2011.0
+ Revision: 661101
- Version 0.91.0

* Tue Aug 17 2010 Anssi Hannula <anssi@mandriva.org> 0.90.4.00.b32-1mdv2011.0
+ Revision: 570717
- new version
- update license tag for policy
- remove name from summary

* Wed Jul 15 2009 Anssi Hannula <anssi@mandriva.org> 0.90.4.00.b31-1mdv2010.0
+ Revision: 396164
- new version
- clarify summary

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Sat Sep 20 2008 Anssi Hannula <anssi@mandriva.org> 0.90.4.00.b24-6mdv2009.0
+ Revision: 286260
- requires java >= 1.6 (fixes #43632)

* Fri Sep 19 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0.90.4.00.b24-5mdv2009.0
+ Revision: 285837
- rebuild

* Fri Aug 08 2008 Thierry Vignaud <tv@mandriva.org> 0.90.4.00.b24-4mdv2009.0
+ Revision: 269012
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Tue Apr 29 2008 Anssi Hannula <anssi@mandriva.org> 0.90.4.00.b24-3mdv2009.0
+ Revision: 198963
+ rebuild (emptylog)

* Tue Apr 29 2008 Anssi Hannula <anssi@mandriva.org> 0.90.4.00.b24-2mdv2009.0
+ Revision: 198915
- fix backportability (for old jar)
- add backportability buildrequires
- 0.90.4.00.b24
- drop gcj precompilation for now due to ICEs
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0.90.4.00-7mdv2008.0
+ Revision: 87345
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Jun 30 2007 Anssi Hannula <anssi@mandriva.org> 0.90.4.00-6mdv2008.0
+ Revision: 46155
- disable cacao hack, now works with gcj
- use only standard menu categories
- workaround gjar upstream bug #32516


* Sat Mar 10 2007 Anssi Hannula <anssi@mandriva.org> 0.90.4.00-5mdv2007.1
+ Revision: 141077
- use cacao instead of jamvm in gui mode

* Mon Mar 05 2007 Anssi Hannula <anssi@mandriva.org> 0.90.4.00-4mdv2007.1
+ Revision: 133354
- fix group
- drop epoch 0
- fix menu categories

* Wed Oct 18 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0:0.90.4.00-3mdv2007.0
+ Revision: 65842
-Add Buildrequires
- import projectx-0.90.4.00-2mdv2007.0

* Sat Sep 02 2006 Anssi Hannula <anssi@mandriva.org> 0:0.90.4.00-2mdv2007.0
- requires jakarta-oro
- more docs
- force jamvm when gui is used, 10x slower but works (gcj is too old)

* Sat Jun 17 2006 Anssi Hannula <anssi@mandriva.org> 0:0.90.4.00-1mdv2007.0
- initial Mandriva release

