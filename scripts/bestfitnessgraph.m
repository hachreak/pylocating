#!/usr/bin/octave -qf

clear all;

arg_list = argv ();
TEMP_DIR = arg_list{1};
ENV = arg_list{2};

verbose = 1;
% ENV=1;
PNUM=str2num(arg_list{3});

% create graph
hold off
for i = (0 : PNUM - 1)
  fname = [TEMP_DIR "/data-" ENV "-" mat2str(i) ".log"]
  data = csvread(fname)
  plot(data(:, 1) - data(1, 1), data(:, 2), 'r-')
  hold on
  plot(data(:, 1) - data(1, 1), data(:, 3), 'b-')
endfor

% save the graph
cmd = ["print -djpg /tmp/image", ENV ".jpg"]
eval(cmd);
