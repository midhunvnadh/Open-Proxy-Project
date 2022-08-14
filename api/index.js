import 'dotenv/config';
import express from 'express';
import { MongoClient } from "mongodb";
const app = express();

const client = new MongoClient(process.env.MONGO_CONN_URL);

app.get('/', (req, res) => {
    const host = req.headers.host
    const protocol = req.protocol
    const server_url = `${protocol}://${host}`
    try {
        return res.status(200).send(
            {
                "endpoints": {
                    "GET /": {
                        "description": "Returns a list of endpoints",
                        "url": `${server_url}/`,
                    },
                    "GET /servers": {
                        "description": "Returns the list of available servers",
                        "url": `${server_url}/servers`,
                    },
                }
            }
        );
    }
    catch (err) {
        return res.status(500).send({ error: true });
    }
});

app.get('/servers', async (req, res) => {
    try {
        const db = client.db("servers");
        const collection = await db.collection('servers').find({ available: true }).project({ _id: 0 }).toArray();
        return res.status(200).send(collection);
    }
    catch (err) {
        return res.status(500).send({ error: true });
    }
})

app.listen(process.env.PORT || 3000, () => {
    console.log('Server is running on port 3000');
})