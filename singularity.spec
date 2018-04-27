# 
# Copyright (c) 2017-2018, SyLabs, Inc. All rights reserved.
# Copyright (c) 2017, SingularityWare, LLC. All rights reserved.
#
# Copyright (c) 2015-2017, Gregory M. Kurtzer. All rights reserved.
# 
# Copyright (c) 2016, The Regents of the University of California, through
# Lawrence Berkeley National Laboratory (subject to receipt of any required
# approvals from the U.S. Dept. of Energy).  All rights reserved.
# 
# This software is licensed under a customized 3-clause BSD license.  Please
# consult LICENSE file distributed with the sources of this project regarding
# your rights to use or distribute this software.
# 
# NOTICE.  This Software was developed under funding from the U.S. Department of
# Energy and the U.S. Government consequently retains certain rights. As such,
# the U.S. Government has been granted for itself and others acting on its
# behalf a paid-up, nonexclusive, irrevocable, worldwide license in the Software
# to reproduce, distribute copies to the public, prepare derivative works, and
# perform publicly and display publicly, and to permit other to do so. 
# 
# 

%global _hardened_build 1

%{!?_rel:%{expand:%%global _rel 1}}

Summary: Application and environment virtualization
Name: singularity
Version: 2.5.0
Release: %{_rel}%{?dist}
# https://spdx.org/licenses/BSD-3-Clause-LBNL.html
License: BSD and LBNL BSD
Group: System Environment/Base
URL: http://singularity.lbl.gov/
Source: https://github.com/singularityware/singularity/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch1: singularity-Python3.patch
ExclusiveOS: linux
BuildRoot: %{?_tmppath}%{!?_tmppath:/var/tmp}/%{name}-%{version}-%{release}-root
BuildRequires: /usr/bin/python3
BuildRequires: automake libtool
BuildRequires: libarchive-devel
%if "%{_target_vendor}" == "suse"
Requires: squashfs
%else
Requires: squashfs-tools
%endif

Requires: %{name}-runtime = %{version}-%{release}

%description
Singularity provides functionality to make portable
containers that can be used across host environments.

%package devel
Summary: Development libraries for Singularity
Group: System Environment/Development

%description devel
Development files for Singularity

%package runtime
Summary: Support for running Singularity containers
Group: System Environment/Base

%description runtime
This package contains support for running containers created
by the %{name} package.

%prep
%setup -q
%patch1 -p0


%build
if [ ! -f configure ]; then
  ./autogen.sh
fi

%configure
%{__make} %{?mflags}


%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT %{?mflags_install}
rm -f $RPM_BUILD_ROOT/%{_libdir}/singularity/lib*.la

%post runtime -p /sbin/ldconfig
%postun runtime -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%license LICENSE.md LICENSE-LBNL.md
%doc examples CONTRIBUTORS.md CONTRIBUTING.md COPYRIGHT.md INSTALL.md LICENSE-LBNL.md LICENSE.md README.md
%attr(0755, root, root) %dir %{_sysconfdir}/singularity
%attr(0644, root, root) %config(noreplace) %{_sysconfdir}/singularity/*

%{_libexecdir}/singularity/cli/apps.*
%{_libexecdir}/singularity/cli/bootstrap.*
%{_libexecdir}/singularity/cli/build.*
%{_libexecdir}/singularity/cli/check.*
%{_libexecdir}/singularity/cli/create.*
%{_libexecdir}/singularity/cli/image.*
%{_libexecdir}/singularity/cli/inspect.*
%{_libexecdir}/singularity/cli/mount.*
%{_libexecdir}/singularity/cli/pull.*
%{_libexecdir}/singularity/cli/selftest.*
%{_libexecdir}/singularity/helpers
%{_libexecdir}/singularity/python

# Binaries
%{_libexecdir}/singularity/bin/builddef
%{_libexecdir}/singularity/bin/cleanupd
%{_libexecdir}/singularity/bin/get-section
%{_libexecdir}/singularity/bin/mount
%{_libexecdir}/singularity/bin/image-type
%{_libexecdir}/singularity/bin/prepheader
%{_libexecdir}/singularity/bin/docker-extract

# Directories
%{_libexecdir}/singularity/bootstrap-scripts

#SUID programs
%attr(4755, root, root) %{_libexecdir}/singularity/bin/mount-suid

%files runtime
%dir %{_libexecdir}/singularity
%dir %{_localstatedir}/singularity
%dir %{_localstatedir}/singularity/mnt
%dir %{_localstatedir}/singularity/mnt/session
%dir %{_localstatedir}/singularity/mnt/container
%dir %{_localstatedir}/singularity/mnt/overlay
%dir %{_localstatedir}/singularity/mnt/final
%{_bindir}/singularity
%{_bindir}/run-singularity
%{_libdir}/singularity/lib*.so.*
%{_libexecdir}/singularity/cli/action_argparser.*
%{_libexecdir}/singularity/cli/exec.*
%{_libexecdir}/singularity/cli/help.*
%{_libexecdir}/singularity/cli/instance.*
%{_libexecdir}/singularity/cli/run.*
%{_libexecdir}/singularity/cli/shell.*
%{_libexecdir}/singularity/cli/test.*
%{_libexecdir}/singularity/bin/action
%{_libexecdir}/singularity/bin/start
%{_libexecdir}/singularity/bin/docker-extract
%{_libexecdir}/singularity/functions
%{_libexecdir}/singularity/handlers
%{_libexecdir}/singularity/image-handler.sh
%dir %{_sysconfdir}/singularity
%config(noreplace) %{_sysconfdir}/singularity/*
%{_mandir}/man1/singularity.1*
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/singularity

#SUID programs
%attr(4755, root, root) %{_libexecdir}/singularity/bin/action-suid
%attr(4755, root, root) %{_libexecdir}/singularity/bin/start-suid

%files devel
%defattr(-, root, root)
%{_libdir}/singularity/lib*.so
%{_libdir}/singularity/lib*.a
%{_includedir}/singularity/*.h


%changelog
* Fri Apr 27 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.0-1
- Update to upstream version 2.5.0

* Mon Apr 16 2018 Dave Dykstra <dwd@fnal.gov> - 2.4.6-1
- Update to upstream version 2.4.6

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun May 21 2017 Dave Love <loveshack@fedoraproject.org> - 2.2.1-3
- Drop patch 13, broken in the merged version
- Fix remaining arch restriction
- Fix configured container_dir

* Thu May 18 2017 Dave Love <loveshack@fedoraproject.org> - 2.2.1-2
- Fix sexec/sexec-suid confusion
- Use _sharedstatedir, not _localstatedir, and make the mnt directories

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
