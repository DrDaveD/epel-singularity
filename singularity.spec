# Based on the bundled version with as few changes as possible.

# Fixme: Move Python bits to the right place
# Fixme: Look at the Python stuff.  It appears to work with both python2
#        and python3, at least, and may not need to obey the Python
#        packaging rules.
# Fixme: Is there any use for devel files?

# Presumably the chdir isn't close enough to the chroot to avoid this
# false positive:
# singularity-runtime.x86_64: E: missing-call-to-chdir-with-chroot /usr/lib64/libsingularity.so.1.0.0

%global _hardened_build 1

# For non-releases
#global commit e7409ff5b279bcee0574576c352f2d251851b9ba

%{?commit:%global shortcommit %(c=%{commit}; echo ${c:0:8})}
%{?commit:%global ver %{commit}}
%{!?commit:%global ver %{version}}

Summary: Enabling "Mobility of Compute" with container based applications
Name: singularity
Version: 2.2.1
Release: 1%{?shortcommit:.git%shortcommit}%{?dist}
License: LBNL BSD
URL: http://singularity.lbl.gov/
%if 0%{?commit:1}
Source: https://codeload.github.com/gmkurtzer/singularity/tar.gz/%{commit}#/%{name}-%{shortcommit}.tar.gz
%else
Source: https://github.com/gmkurtzer/singularity/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
%endif
# Avoid default licensing conditions for changes
Patch1: singularity-copying.patch
# See patches for info
Patch2: singularity-Fix-type-related-errors.patch
Patch3: singularity-Make-syslog-call-format-safe.patch
Patch4: singularity-Add-format-attributes-and-fix-format-error.patch
Patch5: singularity-Fix-variable-reference.patch
Patch6: singularity-Fix-memory-related-warnings.patch
Patch7: singularity-Check-for-gid-0-ownership-as-well-as-uid-0.patch
Patch8: singularity-Use-strtol-not-atoi.patch
Patch9: singularity-Check-for-read-error.patch
Patch10: singularity-Fix-tmp-usage.patch
Patch11: singularity-Configure-for-_GNU_SOURCE-and-make-config.h-first-he.patch
Patch12: singularity-Use-TMPDIR.patch
Patch13: singularity-Drop-privileges-before-printing-messages.patch
Patch14: singularity-Ensure-correct-ownership-for-singularity.conf-on-ins.patch
Patch15: singularity-Replace-malloc-and-strdup-with-xmalloc-and-xstrdup-t.patch
Patch16: singularity-More-config.h-usage-for-C11.patch
Patch17: singularity-Replace-obsolete-AC_PROG_LIBTOOL-with-LT_INIT.patch
Patch18: singularity-Zero-memory-written-to-image.patch

BuildRequires: automake libtool chrpath python2-devel
Requires: %name-runtime
# Necessary at least when bootstrapping f23 on el6
Requires: pyliblzma
# Arguable, but it doesn't pull in much.
Requires: debootstrap
# See above
Requires: /usr/bin/python

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

%package runtime
Summary: Support for running Singularity containers
# For debugging in containers.
Requires: strace ncurses-base
Group: System Environment/Base
ExclusiveArch: x86_64 %ix86
BuildRoot: %{?_tmppath}%{!?_tmppath:/var/tmp}/%{name}-%{version}-%{release}-root

%description runtime
This package contains support for running containers created by %name,
e.g. "singularity exec ...".


%prep
%setup -q -n %{name}-%{ver}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

NO_CONFIGURE=y ./autogen.sh


%build
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/message/6CPVVNZHV3LAGYSMM6EA4JTUCWT2HLWT/
%{!?__global_ldflags: %global __global_ldflags -Wl,-z,relro -Wl,-z,now}
%configure --disable-static %{?fedora:--with-userns}
%{__make} %{?mflags} %{?smp_mflags}


%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT %{?mflags_install}
chmod 644 $RPM_BUILD_ROOT%{_libexecdir}/singularity/cli/*help
rm $RPM_BUILD_ROOT%{_libdir}/*.la
chrpath -d $RPM_BUILD_ROOT%{_libexecdir}/singularity/sexec-suid
chmod 0644 $RPM_BUILD_ROOT%{_libexecdir}/singularity/python/__init__.py \
           $RPM_BUILD_ROOT%{_libexecdir}/singularity/python/docker/__init__.py


%check
# requires sudo and actually a properly-installed version, so not useful
%if %{with check}
sh test.sh
%endif

%post runtime -p /sbin/ldconfig
%postun runtime -p /sbin/ldconfig

%{!?_licensedir:%global license %doc}

%files
%license COPYING LICENSE
%doc AUTHORS README.md TODO examples
# currently empty: NEWS ChangeLog
%{_libexecdir}/singularity/image-bind
%{_libexecdir}/singularity/image-create
%{_libexecdir}/singularity/image-expand
%{_libexecdir}/singularity/cli/bootstrap.*
%{_libexecdir}/singularity/bootstrap
%{_libexecdir}/singularity/cli/copy.*
%{_libexecdir}/singularity/cli/create.*
%{_libexecdir}/singularity/cli/expand.*
%{_libexecdir}/singularity/cli/export.*
%{_libexecdir}/singularity/cli/import.*
%{_libexecdir}/singularity/helpers
%{_libexecdir}/singularity/image-handler.sh
%{_libexecdir}/singularity/python

%files runtime
%license COPYING LICENSE
%dir %{_libexecdir}/singularity
# Required -- see the URL.
%attr(4755, root, root) %{_libexecdir}/singularity/sexec
%{_libexecdir}/singularity/functions
%{_bindir}/singularity
%{_bindir}/run-singularity
%{_libexecdir}/singularity/cli/exec.*
%{_libexecdir}/singularity/cli/run.*
%{_libexecdir}/singularity/cli/mount.*
%{_libexecdir}/singularity/cli/shell.*
%{_libexecdir}/singularity/image-mount
%{_libexecdir}/singularity/cli/singularity.help
%{_libexecdir}/singularity/cli/start.*
%{_libexecdir}/singularity/cli/stop.*
%{_libexecdir}/singularity/cli/test.*
%{_libexecdir}/singularity/get-section
%dir %{_sysconfdir}/singularity
%config(noreplace) %{_sysconfdir}/singularity/*
%{_libdir}/libsingularity.so.*
%exclude %{_libdir}/libsingularity.so
%exclude %{_includedir}/singularity.h
%{_libexecdir}/singularity/sexec-suid
%{_mandir}/man1/singularity.1*
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/singularity


%changelog
* Tue May 16 2017 Dave Love <loveshack@fedoraproject.org> - 2.2.1-1
- New version
- Various spec adjustments for the new version
- Replace the patches with a load more
- Remove RHEL5 rpm-isms

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul 13 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-10
- Modify COPYING to avoid default licensing
- Patches for race warning and return values

* Fri Jul  1 2016 Dave Love <loveshack@fedoraproject.org> - 2.0-9
- Require pyliblzma and debootstrap
- Patch for mounting kernel file systems
- Fix License tag
- Patch for bootstrap

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
