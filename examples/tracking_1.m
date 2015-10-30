#!/usr/bin/octave -qf

clear all;

arg_list = argv ();
LOGFILE = arg_list{1};
IMAGE = arg_list{2};

hold off;
data=dlmread(LOGFILE);

subplot(1,2,1);
plot(data(:,1), data(:,9));

subplot(1,2,2);
plot3(data(:,3), data(:,4), data(:,5));
hold on;
plot3(data(:,6), data(:,7), data(:,8))

cmd = ["print -djpg " IMAGE]
eval(cmd);
