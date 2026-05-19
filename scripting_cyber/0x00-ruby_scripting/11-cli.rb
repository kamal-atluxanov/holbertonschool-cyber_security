#!/usr/bin/env ruby
require 'optparse'

TASKS_FILE = 'tasks.txt'

# Əgər tasks.txt faylı yoxdursa, boş yaradırıq
File.open(TASKS_FILE, 'w').close unless File.exist?(TASKS_FILE)

options = {}

opt_parser = OptionParser.new do |opts|
  opts.banner = "Usage: cli.rb [options]"

  opts.on("-a", "--add TASK", "Add a new task") do |task|
    options[:add] = task
  end

  opts.on("-l", "--list", "List all tasks") do
    options[:list] = true
  end

  opts.on("-r", "--remove INDEX", "Remove a task by index") do |index|
    options[:remove] = index.to_i
  end

  # Optparse avtomatik -h və --help dəstəkləyir, lakin çıxış tam nümunədəki kimi olsun deyə bannerlə işləyir
end

begin
  opt_parser.parse!(ARGV)
rescue OptionParser::InvalidOption, OptionParser::MissingArgument => e
  puts e.validate
  puts opt_parser
  exit 1
end

# --- Task Əlavə Etmək (-a, --add) ---
if options[:add]
  task_name = options[:add]
  File.open(TASKS_FILE, 'a') do |file|
    file.puts(task_name)
  end
  puts "Task '#{task_name}' added."

# --- Taskları Siyahılamaq (-l, --list) ---
elsif options[:list]
  tasks = File.readlines(TASKS_FILE).map(&:strip).reject(&:empty?)
  if tasks.empty?
    puts "No tasks found."
  else
    tasks.each_with_index do |task, index|
      puts "#{index + 1}. #{task}"
    end
  end

# --- Task Silmək (-r, --remove) ---
elsif options[:remove]
  target_index = options[:remove]
  tasks = File.readlines(TASKS_FILE).map(&:strip).reject(&:empty?)

  if target_index > 0 && target_index <= tasks.length
    removed_task = tasks.delete_at(target_index - 1)
    
    # Yenilənmiş siyahını fayla yazırıq
    File.open(TASKS_FILE, 'w') do |file|
      tasks.each { |task| file.puts(task) }
    end
    puts "Task '#{removed_task}' removed."
  else
    puts "Invalid index. Task not found."
  end

# --- Heç bir parametr ötürülməyibsə və ya -h yazılıbsa ---
else
  puts opt_parser
end
