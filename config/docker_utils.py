async def start_docker(docker):
    print("Starting docker.........")
    await docker.start()

async def stop_docker(docker):
    print("Stoping docker......")
    await docker.stop()
    print("Docker has stoped.....")