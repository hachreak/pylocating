#!/usr/bin/octave -qf

clear all;

arg_list = argv ();
DATALOG = arg_list{1};
IMAGE= arg_list{2};

data = dlmread(DATALOG)
plot(data(:,1), data(:,2))

% save the graph
cmd = ["print -djpg " IMAGE]
eval(cmd);
