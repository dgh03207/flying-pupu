#-*- coding:utf-8 -*-
#참고한 좋은 사이트
#https://tmrtkr.tistory.com/83
#챗봇 만드는 사이트
#https://wikidocs.net/78169

import discord
from discord.ext import commands
import youtube_dl
import os
import time
from mutagen.mp3 import MP3
import subprocess
import random
client = commands.Bot(command_prefix = '푸푸')
cnt = 0
waiting_list = ['https://youtu.be/uZ6_ISALjcQ']
hungry_cnt = 0
hungry_text = [
    "야 맛있는거 먹고 싶지 않냐?",
    "나도 배고파...",
    "왜 맨날 배고프냐;",
    "살빼야지^^",
    "나도 머 먹지?",
    "맛있는거 먹고싶다..",
    "즉당히좀 먹어;"
]

# 유튜브 비디오 다운로드 옵션을 특정화하기위해서
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


@client.command()
async def 들어와 (ctx):
    global voice
    #데이터를 모아서 서버에 접속할 수 있도록 함
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = '노가리')
    await voiceChannel.connect()
    voice= discord.utils.get(client.voice_clients, guild = ctx.guild)
    #봇이 우리 채널을 받아올 수 있도록 하는 코드
    # if not voice.is_connected():
    #     await voiceChannel.connect()



@client.command()
async def play_prev(ctx):
    song_there = os.path.isfile("song.mp3")
    if song_there:
        print("노래 재생")
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
    else:
        ctx.send("이전에 재생했던 음악 없으니까, play해서 추가해라")

@client.command()
async def 음악다운 (ctx, url : str):

    try:
        if not str(waiting_list[-1]) == str(url):
            print(waiting_list, "\n링크 재생 : " + url)
            song_there = os.path.isfile("song.mp3")

            if song_there:
                print("  song.mp3파일을 제거하였음")
                os.remove("song.mp3")
            # elif PermissionError:
            #     await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            #
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # 유튜브 링크를 다운로드함
                ydl.download([url])
                time.sleep(3)

            for file in os.listdir("./"):
                if file.endswith(".mp3"):
                    os.rename(file, "song.mp3")
                    time.sleep(3)

            waiting_list.append(url)
            await ctx.send("♬다운 완료했다 재생해라♬")
    except:
        pass




@client.command()
async def play(ctx):
    global voice
    try :
        mp3 = MP3("song.mp3")
        mp3_length = mp3.info.length
        print("mp3 파일 길이는 ", mp3_length)
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        print("노래 듣는 중")

    except PermissionError:
        await ctx.send("노래 재생중이니까 stop부터 하고 play하던가")

@client.command()
async def 나가 (ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = '노가리')
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("나 이미 나갔는데?;; 내쫓지마라ㅡㅡ")

@client.command()
async def pause(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = '노가리')
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("이미 일시정지 됐다.")

@client.command()
async def resume(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = '노가리')
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("오디오 일시정지 안됨")

@client.command()
async def stop(ctx):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = '노가리')
    voice.stop()

@client.command()
async def addlist(ctx,url : str):
    waiting_list.append(url)
    print(waiting_list)

# @client.command()
# async def removesong(ctx):

@client.command()
async def 야(ctx,msg : str):
    global cnt
    global hungry_cnt
    #봇이 스스로 respond하도록 막음
    # if str(ctx.author) == str(client.user):
    #     return
    if  msg.startswith("안녕") or msg.startswith("ㅎㅇ"):
        cnt = cnt+1
        writer = str(ctx.author)
        writer = writer.partition('#')[0]
        if writer == '2ay':
            await ctx.send("안녕하세요 우주천재 이아영님")
        else:
            if cnt > 2:
                await ctx.channel.send("작작불러 이색히야")
            await ctx.send("안녕 "+writer+" 나는 우주천재 이아영이 만든 봇이야")
    elif msg.startswith("미안") or msg.startswith("ㅈㅅ"):
        cnt = 0
        await ctx.send("용서해줄겡")
    elif msg.startswith("따라해"):
        follow_text = str(msg)
        follow_text = follow_text.partition('따라해')
        await ctx.send(follow_text[2])
    elif msg.startswith("배고파"):
        hungry_cnt = hungry_cnt +1
        if hungry_cnt > 10:
            hungry_cnt = 0
            await ctx.send("알았으니까 이제 그만말해")
        message = random.choice(hungry_text)
        await ctx.send(message)


@client.command()
async def 명령어(ctx):
    titles = [
        '음악 재생',
        '대화 하기'
    ]
    contents = [
        '들어와',

    ]
    embed = discord.Embed(
        color =0x4682B4,
        title = "< Commands >",
        description = " *명령어 뭐있는지 알려줌* "
        )
    embed.set_author(name="이아영",icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Video-Game-Controller-Icon-IDV-green.svg/1024px-Video-Game-Controller-Icon-IDV-green.svg.png',)
    embed.add_field(
        name="Music",
        value = "  ex)푸푸play 링크링크\n\n"
                "음악다운 링크주소\n - 유튜브 링크 음악 재생\n\n"
                "음악재생\n - 이전에 재생한 음악 재생\n\n"
                "pause \n - 음악 일시정지\n\n"
                "resume \n - 음악 다시 재생\n\n"
                "stop \n - 음악 정지\n\n")
    embed.add_field(
        name="말하기",
        value = "  ex)푸푸야 안녕\n\n" \
                "안녕 or ㅎㅇ\n\n" \
                "미안 or ㅈㅅ\n\n" \
                "배고파\n\n" \
                "따라해(원하는 문자)\n예)푸푸야 따라해앙뇽")
    await ctx.send(embed=embed)


client.run(본인의 토큰 주소 입력)
