#!/usr/bin/octave -qf

clear all;
verbose = 1;
ENV=1;
PNUM=20;

hold off
for i = (0 : PNUM - 1)
  fname = ["/tmp/data/data-" mat2str(ENV) "-" mat2str(i) ".log"]
  data = csvread(fname)
  plot(data(:, 1) - data(1, 1), data(:, 2), 'r-')
  hold on
  plot(data(:, 1) - data(1, 1), data(:, 3), 'b-')
endfor
print -djpg /tmp/image.jpg
