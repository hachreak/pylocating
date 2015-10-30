#!/usr/bin/octave -qf

clear all;

hold off;
data=dlmread("logs/tracking_1-movingpoint.log");

subplot(1,2,1);
plot(data(:,1), data(:,9));

subplot(1,2,2);
plot3(data(:,3), data(:,4), data(:,5));
hold on;
plot3(data(:,6), data(:,7), data(:,8))

print -djpg /tmp/tracking_1.jpg
