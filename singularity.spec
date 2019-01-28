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

%define singgopath src/github.com/sylabs/singularity

# Disable debugsource packages; otherwise it ends up with an empty %files
#   file in debugsourcefiles.list on Fedora
%undefine _debugsource_packages

Summary: Application and environment virtualization
Name: singularity
Version: 3.0.3
Release: 1%{?dist}
# https://spdx.org/licenses/BSD-3-Clause-LBNL.html
License: BSD-3-Clause-LBNL
URL: https://www.sylabs.io/singularity/
Source: %{name}-%{version}.tar.gz
ExclusiveOS: linux
BuildRoot: %{?_tmppath}%{!?_tmppath:/var/tmp}/%{name}-%{version}-%{release}-root
%if "%{_target_vendor}" == "suse"
BuildRequires: go
%else
BuildRequires: golang
%endif
BuildRequires: wget
BuildRequires: git
BuildRequires: gcc
BuildRequires: make
BuildRequires: libuuid-devel
BuildRequires: openssl-devel
%if ! 0%{?el6}
BuildRequires: libseccomp-devel
%endif
%if "%{_target_vendor}" == "suse"
Requires: squashfs
%else
Requires: squashfs-tools
%endif

# there's no golang for ppc64, just ppc64le
ExcludeArch: ppc64

Provides: %{name}-runtime
Obsoletes: %{name}-runtime

%description
Singularity provides functionality to make portable
containers that can be used across host environments.

%debug_package

%prep
# Create our build root
rm -rf %{name}-%{version}
mkdir %{name}-%{version}

%build
cd %{name}-%{version}

mkdir -p gopath/%{singgopath}
tar -C "gopath/src/github.com/sylabs/" -xf "%SOURCE0"

export GOPATH=$PWD/gopath
export PATH=$GOPATH/bin:$PATH
cd $GOPATH/%{singgopath}

./mconfig -V %{version}-%{release} --prefix=%{_prefix} --exec-prefix=%{_exec_prefix} \
	--bindir=%{_bindir} --libexecdir=%{_libexecdir} --sysconfdir=%{_sysconfdir} \
	--sharedstatedir=%{_sharedstatedir} --localstatedir=%{_localstatedir} \
	--libdir=%{_libdir}

cd builddir
make old_config=

%install
cd %{name}-%{version}

export GOPATH=$PWD/gopath
export PATH=$GOPATH/bin:$PATH
cd $GOPATH/%{singgopath}/builddir

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
make DESTDIR=$RPM_BUILD_ROOT install man
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/singularity/actions/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%attr(4755, root, root) %{_libexecdir}/singularity/bin/starter-suid
%{_bindir}/*
%dir %{_libexecdir}/singularity
%{_libexecdir}/singularity/bin/starter
%{_libexecdir}/singularity/cni/*
%dir %{_sysconfdir}/singularity
%config(noreplace) %{_sysconfdir}/singularity/*
%attr(755, root, root) %{_sysconfdir}/singularity/actions/exec
%attr(755, root, root) %{_sysconfdir}/singularity/actions/run
%attr(755, root, root) %{_sysconfdir}/singularity/actions/shell
%attr(755, root, root) %{_sysconfdir}/singularity/actions/start
%attr(755, root, root) %{_sysconfdir}/singularity/actions/test
%dir %{_sysconfdir}/bash_completion.d
%{_sysconfdir}/bash_completion.d/*
%dir %{_localstatedir}/singularity
%dir %{_localstatedir}/singularity/mnt
%dir %{_localstatedir}/singularity/mnt/session
# XXX: Not great since we can't control this location...
%{_mandir}/man1/*


%changelog
* Tue Jan 22 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.0.3-1
- Update to upstream 3.0.3-1 release.

* Fri Jan 18 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.0.3-rc2
- Update to upstream 3.0.3-rc2

* Wed Jan 16 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.0.3-rc1
- Update to upstream 3.0.3-rc1

* Wed Jan 09 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.0.2-1.2
- Add patch for PR 2531

* Mon Jan 07 2019 Dave Dykstra <dwd@fedoraproject.org> - 3.0.2-1.1
- Update to upstream 3.0.2
- Added patches for PRs 2472, 2478, 2481

* Tue Dec 11 2018 Dave Dykstra <dwd@fedoraproject.org> - 2.6.1-1.1
- Update to released upstream 2.6.1

* Tue Aug 07 2018 Dave Dykstra <dwd@fnal.gov> - 2.6.0-1.1
- Update to released upstream 2.6.0
- Rename PR 1638 to 1817
- Rename PR 1762 to 1818
- Note that PR 1324 was also renamed, to 1819

* Tue Jul 24 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.999-1.4
- Move the Requires /usr/bin/python3 to be under %package runtime instead
  of under its %description.

* Tue Jul 24 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.999-1.3
- Move the BuildRequires /usr/bin/python3 back to the primary package,
  because otherwise it doesn't get installed at build time.  Leave
  the Requires on the runtime subpackage.
- Add singularity.abignore to avoid warnings from abipkgdiff.

* Tue Jul 24 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.999-1.2
- Add PR #1324 which makes the docker:// and shub:// URLs work with only
  the runtime subpackage.  All the changes are to this file so it does
  not add a patch.  Moves python files to the runtime subpackage, so the
  BuildRequires & Requires /usr/bin/python3 go back there as well.
- Improve the underlay option comment in singularity.conf as found in
  the current version of PR #1638.

* Tue Jul 24 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.999-1.1
- Update to upstream 2.5.999, which is tagged as 2.6.0-rc2.
- Disable the underlay feature by default
- Move the BuildRequires: /usr/bin/python3 back to the singularity package
  because there is no python in singularity-runtime.
- Add an additional Requires: /usr/bin/python3 for install time.

* Mon Jul 16 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.99-1.1
- Update to upstream 2.5.99, which is tagged as 2.6.0-rc1.
- Switch to using internally defined require_python3, which is true unless
  %{osg} is defined, to decide whether or not to require python3.
- Get python3 patch from PR #1762 instead of custom defined.
- Move /usr/bin/python3 BuildRequires to singularity-runtime subpackage.
- Apply PR #1638, which adds the underlay feature.

- Only require python3 if %{py3_dist} macro defined

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.2-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.2-1
- Update to upstream high severity security release 2.5.2.   See
  https://github.com/singularityware/singularity/releases/tag/2.5.2
  and CVE #2018-12021.
- Only require python3 if %{py3_dist} macro defined

* Fri May 04 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.1-1
- Update to upstream version 2.5.1

* Fri Apr 27 2018 Dave Dykstra <dwd@fnal.gov> - 2.5.0-1
- Update to upstream version 2.5.0

* Mon Apr 16 2018 Dave Dykstra <dwd@fnal.gov> - 2.4.6-1
- Update to upstream version 2.4.6

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

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

