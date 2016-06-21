# Based on the bundled version with as few changes as possible.
# The el5 features are required.
# See https://github.com/gmkurtzer/singularity/issues/64 about some
# rpmlint warnings.

%global _hardened_build 1

# Run %%check, which requires sudo
%bcond_with check

# For non-releases
#global commit e7409ff5b279bcee0574576c352f2d251851b9ba

%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:8})}
%{?commit:%global ver %{commit}}
%{!?commit:%global ver %{version}}

Summary: Enabling "Mobility of Compute" with container based applications
Name: singularity
Version: 2.0
Release: 8%{?shortcommit:.git%shortcommit}%{?dist}
License: BSD
Group: System Environment/Base
URL: http://singularity.lbl.gov/
%if 0%{?commit:1}
Source: https://codeload.github.com/gmkurtzer/singularity/tar.gz/%{commit}#/%{name}-%{shortcommit}.tar.gz
%else
Source: https://github.com/gmkurtzer/singularity/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif
# Port upstream changes for <https://github.com/gmkurtzer/singularity/issues/64>
Patch1: singularity-sec.patch
# Better handling of yum/dnf <https://github.com/loveshack/singularity/commit/3322d29bf9323194ddaaddc0f082595ca9f4ad76>
Patch2: singularity-yum.patch
# DTRT for rpm release package <https://github.com/gmkurtzer/singularity/commit/327c4f8d35d576ba754c0fa4434555d20878e8a4>
Patch3: singularity-release.patch
# Fedora example <https://github.com/gmkurtzer/singularity/commit/95cb0a4b763c6eb375633c0bc10d6b322bf77be4>
Patch4: singularity-fedora.patch
# Ensure directory exists before copying file to it <https://github.com/gmkurtzer/singularity/commit/4e0f8575f47e8abb59d0869d4b6ade5c2399b6f3
Patch5: singularity-mkdir.patch
BuildRequires: automake libtool
# For debugging in containers.
Requires: strace ncurses-base
# ftrace manipulates registers; it's not currently used, but will be
# resurrected, and configure checks the arch.
ExclusiveArch: x86_64 %ix86
BuildRoot: %{?_tmppath}%{!?_tmppath:/var/tmp}/%{name}-%{version}-%{release}-root

%description 
Singularity is a container platform focused on supporting "Mobility of
Compute".

Mobility of Compute encapsulates the development to compute model
where developers can work in an environment of their choosing and
creation and when the developer needs additional compute resources,
this environment can easily be copied and executed on other platforms.
Additionally as the primary use case for Singularity is targeted
towards computational portability, many of the barriers to entry of
other container solutions do not apply to Singularity making it an
ideal solution for users (both computational and non-computational)
and HPC centers.

%prep
%setup -q -n %{name}-%{ver}
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
NO_CONFIGURE=y ./autogen.sh


%build
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/6CPVVNZHV3LAGYSMM6EA4JTUCWT2HLWT/
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro -Wl,-z,now}
%configure 
%{__make} %{?mflags} %{?smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT %{?mflags_install}
chmod 644 $RPM_BUILD_ROOT%{_libexecdir}/singularity/cli/*{summary,help}


%check
# requires sudo
%if %{with check}
sh test.sh
%endif


%clean
rm -rf $RPM_BUILD_ROOT


%{!?_licensedir:%global license %doc}

%files
%license COPYING LICENSE
%doc AUTHORS README.md TODO examples
# currently empty: NEWS ChangeLog
%dir %{_libexecdir}/singularity
# Required -- see the URL.
%attr(4755, root, root) %{_libexecdir}/singularity/sexec
%{_libexecdir}/singularity/functions
# Not used in this version (but to be resurrected in future)
%exclude %{_libexecdir}/singularity/ftrace
%exclude %{_libexecdir}/singularity/ftype
%{_libexecdir}/singularity/mods
%{_libexecdir}/singularity/cli
%{_libexecdir}/singularity/bootstrap.sh
%{_libexecdir}/singularity/copy.sh
%{_libexecdir}/singularity/image-bind
%{_libexecdir}/singularity/image-create
%{_libexecdir}/singularity/image-expand
%{_libexecdir}/singularity/image-mount
%{_bindir}/singularity
%{_bindir}/run-singularity
%dir %{_sysconfdir}/singularity
%config(noreplace) %{_sysconfdir}/singularity/*


%changelog
* Tue Jun 21 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-8
- Revert part of -yum patch

* Fri Jun 17 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-7
- Actually apply patch5

* Thu Jun 16 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-6
- Patches for yum/dnf usage, Fedora example, installing rpm release package,
  creating directories
- Change URL

* Sat Jun 11 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-5
- Modify snapshot bits per review instructions

* Wed Jun  8 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-5
- Patch for rpmlint warnings

* Tue Jun  7 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-4
- Revert last change; configure limits arch, and ftrace to be used again

* Tue Jun  7 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-3
- Don't build ftrace, ftype and remove the arch restriction

* Mon Jun  6 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-2
- Ship LICENSE, examples

* Thu Jun  2 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-1
- New version
- Replace spec features for el5
- Exclude ftrace, ftype

* Fri Apr 29 2016 Dave Love <loveshack@fedoraproject.org> - 1.0-6.e7409ff5
- Updated snapshot

* Thu Apr 21 2016 Dave Love <loveshack@fedoraproject.org> - 1.0-5.20160420
- Don't require which

* Thu Apr 21 2016 Dave Love <loveshack@fedoraproject.org> - 1.0-5.20160420
- Snapshot version
- Remove resolver patch
- Add hardening ldflags

* Wed Apr 20 2016 Dave Love <loveshack@fedoraproject.org> - 1.0-4
- Take description from readme

* Mon Apr 18 2016 Dave Love <loveshack@fedoraproject.org> - 1.0-3
- Patch for missing utils for debug on el6
- More resolver changes

* Sat Apr 16 2016 Dave Love <loveshack@fedoraproject.org> - 1.0-2
- Fix running text resolvers
- Don't configure twice

* Fri Apr 15 2016 Dave Love <loveshack@fedoraproject.org> - 1.0-1
- New version
- BR automake, libtool and run autogen

* Wed Apr 06 2016 Dave Love <loveshack@fedoraproject.org> - 1.0-0.1.20150405
- Initial version adapted for Fedora as minimally as possible from
  bundled spec (can't run on el5)
