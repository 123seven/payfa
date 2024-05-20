import {PageContainer, ProCard, ProDescriptions,} from '@ant-design/pro-components';
import {Button,} from 'antd';
import React from 'react';

const MonitorList = () => {

  return (
    <ProDescriptions

      title="高级定义列表request columns"
      request={async () => {
        return Promise.resolve({
          success: true,
          data: {
            date: '20200809',
            money: '1212100',
            money2: -12345.33,
            state: 'all',
            switch: true,
            state2: 'open',
          },
        });
      }}
      columns={[
        {
          title: 'ID',
          key: 'text',
          dataIndex: 'id',
        },
        {
          title: '状态',
          key: 'state',
          dataIndex: 'state',
          valueType: 'select',
          valueEnum: {
            all: {text: '全部', status: 'Default'},
            open: {
              text: '未解决',
              status: 'Error',
            },
            closed: {
              text: '已解决',
              status: 'Success',
            },
          },
        },

        {
          title: '时间',
          key: 'date',
          dataIndex: 'date',
          valueType: 'date',
        },

        {
          title: '开关',
          key: 'switch',
          dataIndex: 'switch',
          valueType: 'switch',
        },
        {
          title: 'money',
          key: 'money',
          dataIndex: 'money',
          valueType: 'money',
          fieldProps: {
            moneySymbol: '$',
          },
        },
        {
          title: '操作',
          valueType: 'option',
          render: () => [
            <a target="_blank" rel="noopener noreferrer" key="link">
              链路
            </a>,
            <a target="_blank" rel="noopener noreferrer" key="warning">
              报警
            </a>,
            <a target="_blank" rel="noopener noreferrer" key="view">
              查看
            </a>,
          ],
        },
      ]}
    >
    </ProDescriptions>
  );
};

const Admin: React.FC = () => {

  return (
    <PageContainer
      header={{
        extra: [
          <Button key="3" type="primary">
            新建
          </Button>,
        ],
      }}

    >
      <ProCard
        style={{marginBlockStart: 16}}
        gutter={[16, 16]}
        wrap
      >
        <ProCard
          layout="center"
          bordered>
          <MonitorList/>
        </ProCard>

        <ProCard
          layout="center"
          bordered>
          <MonitorList/>
        </ProCard>
      </ProCard>
    </PageContainer>
  );
};

export default Admin;
