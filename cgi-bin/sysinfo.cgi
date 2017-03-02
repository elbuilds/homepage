#!/usr/bin/env perl
# ==============================================================================
# This cgi show system information.
# ==============================================================================

package main;

use strict;
use warnings;
use 5.010;
use POSIX qw(uname);
use Sys::Info;
use Sys::MemInfo qw(totalmem freemem totalswap freeswap);
use Sys::Uptime;
use Filesys::DiskFree;
use CGI qw(:standard :html3);

MAIN: {
  my @rows = th [];
  my $info = Sys::Info->new;
  my $disk = Filesys::DiskFree->new;
  $disk->df;
  my $kernel = join " ", (&uname)[0,2,4];
  my $httpd = $info->httpd;
  my $perl = $info->perl;
  my $uptime = Sys::Uptime::uptime () / 60**2;
  my $cpu = $info->device ('CPU');
  my $cpuIdentify = scalar $cpu->identify || 'N/A';
  my $cpuSpeed = $cpu->speed || 'N/A';
  my $cpuCount = $cpu->count || 1;
  my $cpuLoad = $cpu->load  || 0;
  my $memtotal = &totalmem / 1024**2;
  my $memused = $memtotal - &freemem / 1024**2;
  my $swaptotal = &totalswap / 1024**2;
  my $swapused  = $swaptotal - &freeswap / 1024**2;
  my $homedevice = $disk->device ("/home");
  my $hometotal = $disk->total ("/home") / 1024**2;
  my $homeused = $disk->used ("/home") / 1024**2;

  say header ('text/html');
  say start_html (-title => "SYSTEM INFOMATION FOR ELBUILDS.WEBSITE"), hr;

  if ($CGI::VERSION < 4.08) {
    say 'Your CGI.pm is too old to work, visit ',
          a ({ -href=>'https://metacpan.org/pod/distribution/CGI/lib/CGI.pod' },
            'CPAN'),
          ' to get a new one.';
    say hr, end_html;
    exit 1;
  }

  $httpd and push @rows, td ['Apache version', $httpd];
  push @rows, td ['Kernel version', $kernel];
  push @rows, td ['Perl version', $perl];
  push @rows, td ['CGI.pm version', $CGI::VERSION];
  push @rows, td ['Uptime', sprintf ('%.2f h', $uptime)];
  push @rows, td ['CPU indentify', $cpuIdentify];
  push @rows, td ['CPU count', $cpuCount];
  push @rows, td ['CPU speed', "${cpuSpeed} MHz"];
  push @rows, td ['CPU load', "${cpuLoad}%"];
  push @rows, td ["Memory total", sprintf ('%.2f MiB', $memtotal)];
  push @rows, td ["Memory used", sprintf ('%.2f MiB', $memused)];
  push @rows, td ["Swap total", sprintf ('%.2f MiB', $swaptotal)];
  push @rows, td ["Swap used", sprintf ('%.2f MiB', $swapused)];
  push @rows, td ["/home device", $homedevice];
  push @rows, td ["/home total", sprintf ('%.2f MiB', $hometotal)];
  push @rows, td ["/home used", sprintf ('%.2f MiB', $homeused)];

  say table { -border => undef, -width => '50%' },
          caption b 'System Information for elbuilds.website',
          Tr \@rows;

  say hr, end_html;
}

1;

=encoding utf-8

=head1 sysinfo.cgi

This cgi show system information.

=cut

