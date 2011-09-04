%global priority    65-0
%global fontname    baekmuk-ttf
%define archivename %{fontname}-%{version}
%define common_desc \
This package provides the free Korean TrueType fonts.

%define gsdir          %{_datadir}/ghostscript/conf.d
%define catalogue      %{_sysconfdir}/X11/fontpath.d

Name:           %{fontname}-fonts
Version:        2.2
Release:        28%{?dist}
Summary:        Free Korean TrueType fonts

Group:          User Interface/X
License:        Baekmuk
URL:            http://kldp.net/projects/baekmuk/
Source0:        http://kldp.net/frs/download.php/1429/%{archivename}.tar.gz
Source1:        FAPIcidfmap.ko
Source2:        cidfmap.ko
Source3:        baekmuk-ttf-batang.conf
Source4:        baekmuk-ttf-dotum.conf
Source5:        baekmuk-ttf-gulim.conf
Source6:        baekmuk-ttf-hline.conf

Obsoletes:      fonts-korean <= 2.2-23
Provides:       fonts-korean = 2.2-25

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  fontpackages-devel >= 1.13 , xorg-x11-font-utils
BuildRequires:  ttmkfdir >= 3.0.6

%description
%common_desc

%package -n %{fontname}-batang-fonts
Summary:        Korean Baekmuk TrueType Batang typeface
Group:          User Interface/X
Obsoletes:      %{name}-batang < 2.2-13
Provides:       %{name}-batang = 2.2-25
Requires:       %{fontname}-fonts-common = %{version}-%{release}

%description -n %{fontname}-batang-fonts
%common_desc

Batang is Korean TrueType font in Serif typeface.

%_font_pkg -n batang -f *-%{fontname}-batang*.conf batang.ttf

%package -n %{fontname}-dotum-fonts
Summary:        Korean Baekmuk TrueType Dotum typeface
Group:          User Interface/X
Obsoletes:      %{name}-dotum < 2.2-13 
Provides:       %{name}-dotum = %{version}-%{release}
Requires:       %{fontname}-fonts-common = %{version}-%{release}

%description -n %{fontname}-dotum-fonts
%common_desc

Dotum is Korean TrueType font in San-serif typeface.

%_font_pkg -n dotum -f *-%{fontname}-dotum*.conf dotum.ttf

%package -n %{fontname}-gulim-fonts
Summary:        Korean Baekmuk TrueType Gulim typeface
Group:          User Interface/X
Obsoletes:      %{name}-gulim < 2.2-13
Provides:       %{name}-gulim = 2.2-25
Requires:       %{fontname}-fonts-common = %{version}-%{release}

%description -n %{fontname}-gulim-fonts
%common_desc

Gulim is Korean TrueType font in Monospace typeface.

%_font_pkg -n gulim -f *-%{fontname}-gulim*.conf gulim.ttf

%package -n %{fontname}-hline-fonts
Summary:        Korean Baekmuk TrueType Headline typeface
Group:          User Interface/X
Obsoletes:      %{name}-hline < 2.2-13
Provides:       %{name}-hline = 2.2-25
Requires:       %{fontname}-fonts-common = %{version}-%{release}

%description -n %{fontname}-hline-fonts
%common_desc

Headline is Korean TrueType font in Black face.

%_font_pkg -n hline -f *-%{fontname}-hline*.conf hline.ttf

%package -n %{fontname}-fonts-ghostscript
Summary:        Ghostscript files for Korean Baekmuk TrueType fonts
Group:          User Interface/X
Requires:       ghostscript >= 8.63-4
Requires:       %{fontname}-batang-fonts = %{version}-%{release} 
Requires:       %{fontname}-dotum-fonts = %{version}-%{release} 
Requires:       %{fontname}-gulim-fonts = %{version}-%{release} 
Requires:       %{fontname}-hline-fonts = %{version}-%{release} 

%description -n %{fontname}-fonts-ghostscript
%common_desc

This is ghostscript files for Baekmuk Korean TrueType fonts.

%files -n %{fontname}-fonts-ghostscript
%defattr(-,root,root,-)
%{gsdir}/cidfmap.ko
%{gsdir}/FAPIcidfmap.ko

%package -n %{fontname}-fonts-common
Summary:        Common files for Korean Baekmuk TrueType fonts
Group:          User Interface/X
Obsoletes:      ttfonts-ko < 1.0.11-33, fonts-korean < 2.2-5
Obsoletes:      baekmuk-ttf-common-fonts < 2.2-17
Provides:       baekmuk-ttf-common-fonts = %{version}-%{release}
Provides:       fonts-korean = %{version}-%{release}
Provides:       ttfonts-ko = %{version}-%{release} 
Requires:       fontpackages-filesystem >= 1.13
BuildRequires:  fontpackages-filesystem >= 1.13

%description -n %{fontname}-fonts-common
%common_desc

This is common files for Baekmuk Korean TrueType fonts.

%files -n %{fontname}-fonts-common
%defattr(0644,root,root,0755)
%doc COPYRIGHT COPYRIGHT.ko README
%dir %{_fontdir}
%verify(not md5 size mtime) %{_fontdir}/fonts.dir
%verify(not md5 size mtime) %{_fontdir}/fonts.scale
%verify(not md5 size mtime) %{catalogue}/%{fontname}

%prep
%setup -q -n %{archivename}

%build
%{nil}

%install
%__rm -rf %{buildroot}

# font
%__install -d -m 0755 %{buildroot}%{_fontdir}
for i in batang dotum gulim hline; do
  %__install -p -m 0644 ttf/$i.ttf %{buildroot}%{_fontdir}
done

# fontconfig conf
%__install -m 0755 -d %{buildroot}%{_fontconfig_templatedir}
%__install -m 0755 -d %{buildroot}%{_fontconfig_confdir}
cd ../
for fconf in %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6}
do
    %__install -m 0644 $fconf %{buildroot}%{_fontconfig_templatedir}/%{priority}-$(basename $fconf)
    %__ln_s %{_fontconfig_templatedir}/%{priority}-$(basename $fconf) \
        %{buildroot}%{_fontconfig_confdir}/%{priority}-$(basename $fconf)
done
cd -

# fonts.{scale,dir}
%{_bindir}/ttmkfdir -d %{buildroot}%{_fontdir} \
  -o %{buildroot}%{_fontdir}/fonts.scale
%{_bindir}/mkfontdir %{buildroot}%{_fontdir}

# ghostscript
%__install -d -m 0755 %{buildroot}%{gsdir}
%__install -p -m 0644 %{SOURCE1} %{buildroot}%{gsdir}/
%__install -p -m 0644 %{SOURCE2} %{buildroot}%{gsdir}/

# catalogue
%__install -d -m 0755 %{buildroot}%{catalogue}
%__ln_s %{_fontdir} %{buildroot}%{catalogue}/%{fontname}

# convert Korean copyright file to utf8
%{_bindir}/iconv -f EUC-KR -t UTF-8 COPYRIGHT.ks > COPYRIGHT.ko

%clean
%__rm -rf %{buildroot}

%changelog
* Wed May 26 2010 Akira TAGOH <tagoh@redhat.com> - 2.2-28
- Improve the fontconfig config file to match ko-kr as well. (#586894)
- Update the priority to avoid overriding 65-nonlatin.conf.
- Fix a typo in the spec file.

* Tue May 04 2010 Caius 'kaio' Chance <cchance@redhat.com> - 2.2-26
- Resolves: rhbz#586849.
- Fixed package dependencies.

* Fri Apr 30 2010 Caius 'kaio' Chance <cchance@redhat.com> - 2.2-25
- Resolves: rhbz#586849.
- Fixed package dependencies.

* Thu Apr 29 2010 Caius 'kaio' Chance <cchance@redhat.com> - 2.2-24
- Resolves: rhbz#586849.
- Fixed lang-specific overrides rule doesn't work as expected.

* Wed Jan 13 2010 Caius 'kaio' Chance <cchance@redhat.com> - 2.2-23.el6
- Resolves: rhbz#554953
- Fixed rpmlint errors. 

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.2-22.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 08 2009 Caius 'kaio' Chance <cchance@redhat.com> - 2.2-21.fc11
- Resolves: rhbz#483327 (Fixed unowned directories.)

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 03 2009 Caius Chance <cchance@redhat.com> - 2.2-19.fc11
- Resolves: rhbz#483327
- Reowned font directory by subpackage -common.
- Splited ghostscript files to subpackage -ghostscript.
- Updated paths in ghostscript files.

* Mon Feb 02 2009 Caius Chance <cchance@redhat.com> - 2.2-18.fc11
- Updated fontconfig .conf files based on fontpackages templates.

* Tue Jan 27 2009 Caius Chance <cchance@redhat.com> - 2.2-17.fc11
- Resolves: rhbz#477332
- Fixed obsoletion of baekmuk-ttf-common-fonts.

* Thu Jan 22 2009 Caius Chance <cchance@redhat.com> - 2.2-16.fc11
- Resolves: rhbz#477332
- Refined dependencies.

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 2.2-15.fc11
- Fix busted inter-subpackage dependencies

* Tue Jan 20 2009 Caius Chance <cchance@redhat.com> - 2.2-14.fc11
- Resolves: rhbz#477332
- Refined according to Mailhot's comments (477410) on liberaton fonts.

* Mon Jan 19 2009 Caius Chance <cchance@redhat.com> - 2.2-13.fc11
- Resolves: rhbz#477332
- Package renaming for post-1.13 fontpackages.

* Fri Jan 16 2009 Caius Chance <cchance@redhat.com> - 2.2-12.fc11
- Resolves: rhbz#477332 (Repatched buildsys error.)

* Fri Jan 16 2009 Caius Chance <cchance@redhat.com> - 2.2-11.fc11
- Resolves: rhbz#477332 (Included macro _font_pkg and created fontconfig .conf files.)

* Fri Jan 09 2009 Caius Chance <cchance@redhat.com> - 2.2-10.fc11
- Resolves: rhbz#477332 (Converted to new font packaging guidelines.)

* Mon Jun 30 2008 Caius Chance <cchance@redhat.com> - 2.2-9.fc10
- Refine obsoletes tag version-release specific.

* Mon Jun 30 2008 Caius Chance <cchance@redhat.com> - 2.2-8.fc10
- Resolves: rhbz#453080 (fonts-korean is deprecated and should be removed.)

* Wed Nov 14 2007 Jens Petersen <petersen@redhat.com> - 2.2-7
- better url
- use fontname and fontdir macros

* Mon Sep 24 2007 Jens Petersen <petersen@redhat.com> - 2.2-6
- convert Korean copyright file to utf8 (Mamoru Tasaka, #300651)

* Mon Sep 24 2007 Jens Petersen <petersen@redhat.com> - 2.2-5
- more fixes from Mamoru Tasaka, #300651:
- make common subpackage own ghostscript conf.d
- conflict with previous fonts-korean
- update CID font maps

* Mon Sep 24 2007 Jens Petersen <petersen@redhat.com> - 2.2-4
- preserve timestamps of installed files (Mamoru Tasaka, #300651)
- add a common subpackage for shared files (Mamoru Tasaka, #300651)

* Mon Sep 24 2007 Jens Petersen <petersen@redhat.com> - 2.2-3
- do not provide ttfonts-ko in subpackages (Mamoru Tasaka, #300651)

* Sat Sep 22 2007 Jens Petersen <petersen@redhat.com> - 2.2-2
- license is now designated Baekmuk

* Sat Sep 22 2007 Jens Petersen <petersen@redhat.com> - 2.2-1
- new package separated from fonts-korean (#253155)
