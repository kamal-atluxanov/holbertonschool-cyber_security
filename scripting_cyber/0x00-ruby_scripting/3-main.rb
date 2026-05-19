require 'json'

def count_user_ids(path)
  # 1. JSON faylını oxuyuruq və analiz (parse) edirik
  file_content = File.read(path)
  data = JSON.parse(file_content)

  # 2. Hər bir userId-nin neçə dəfə təkrarlandığını saymaq üçün Hash yaradırıq
  # Default olaraq tapılmayan açarların dəyərini 0 təyin edirik
  counts = Hash.new(0)

  data.each do |item|
    if item['userId']
      counts[item['userId']] += 1
    end
  end

  # 3. Nəticəni ekrana çıxarırıq (Məsələn, "1: 10")
  counts.each do |user_id, count|
    puts "#{user_id}: #{count}"
  end
rescue Errno::ENOENT
  puts "Xəta: #{path} faylı tapılmadı!"
rescue JSON::ParserError
  puts "Xəta: Fayl düzgün JSON formatında deyil!"
end
