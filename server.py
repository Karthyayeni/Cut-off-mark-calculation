import asyncio
import websockets
import json

async def calculate_cutoff(websocket, path):
    print("Client connected.")
    try:
        data = await websocket.recv()
        print(f"Received data: {data}")
        data = json.loads(data)
        response = {}

        scheme = data['scheme']
        if scheme == "Agri":
            physics = data['physics']
            chemistry = data['chemistry']
            biology = data['biology']
            cutoff = (physics * 0.5) + (chemistry * 0.5) + biology
            response['cutoff'] = cutoff
        elif scheme == "Engineering":
            physics = data['physics']
            chemistry = data['chemistry']
            maths = data['maths']
            cutoff = (physics * 0.5) + (chemistry * 0.5) + maths
            response['cutoff'] = cutoff
        elif scheme == "TNPSC":
            candidate_marks = data['candidate_marks']
            max_marks = 300
            cutoff = (candidate_marks / max_marks) * 100
            response['cutoff'] = cutoff
        elif scheme == "UPSC":
            if data['stage'] == "Prelims":
                gs_marks = data['gs_marks']
                max_marks = 200
                cutoff = (gs_marks / max_marks) * 100
                response['cutoff'] = cutoff
            else:
                mains_marks = data['mains_marks']
                interview_marks = data['interview_marks']
                total_marks = mains_marks + interview_marks
                max_total = 2025
                cutoff = (total_marks / max_total) * 100
                response['cutoff'] = cutoff
        elif scheme == "CAT":
            total_candidates = data['total_candidates']
            candidates_below = data['candidates_below']
            percentile = (total_candidates / (candidates_below + 1)) * 100
            response['cutoff'] = percentile

        await websocket.send(json.dumps(response))
        print(f"Sent response: {response}")

    except Exception as e:
        response['error'] = str(e)
        await websocket.send(json.dumps(response))
        print(f"Error: {str(e)}")

async def start_server():
    server = await websockets.serve(calculate_cutoff, "localhost", 6789)
    print("Server started at ws://localhost:6789")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(start_server())
