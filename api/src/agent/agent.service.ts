import { Injectable } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class AgentService {
  private agentUrl = process.env.AGENT_URL || 'http://agent:8000';

  async checkCommunication() {
    try {
      console.log(this.agentUrl);

      const response = await axios.post(`${this.agentUrl}/request`, {
        message: 'Hello from API',
      });

      return response.data;
    } catch (error) {
      console.error('Error communicating with Agent:', error);
      throw new Error('Agent service is unavailable');
    }
  }
}
