import { Injectable } from '@nestjs/common';
import { AgentService } from './agent/agent.service';

@Injectable()
export class AppService {
  constructor(private readonly agentService: AgentService) {}

  async getHello(data: any): Promise<any> {
    return await this.agentService.checkCommunication(data);
  }
}
