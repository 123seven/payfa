import type {ActionType} from '@ant-design/pro-components';
import {ModalForm, PageContainer, ProFormText, ProFormUploadDragger, ProList,} from '@ant-design/pro-components';
import {Badge, Button, Form, message} from 'antd';
import React, {useRef, useState} from 'react';

const dataSource = [
  {
    id: 1,
    name: '名称1',
    qrcode: "",
    desc: '系统性的沉淀B端知识体系',
    content: [
      {
        label: '今日订单数',
        value: 2903,
      },
      {
        label: '今日金额',
        value: 3720,
      },
      {
        label: '总订单数',
        value: 3720,
      },
      {
        label: '总金额',
        value: 3720,
      },
      {
        label: '状态',
        value: '启用',
        status: 'success',
      },
    ],
  },
  {
    id: 2,
    name: '名称2',
    qrcode: "",
    desc: '系统性的沉淀B端知识体系',
    content: [
      {
        label: '今日订单数',
        value: 2903,
      },
      {
        label: '今日金额',
        value: 3720,
      },
      {
        label: '总订单数',
        value: 3720,
      },
      {
        label: '总金额',
        value: 3720,
      },
      {
        label: '状态',
        value: '启用',
        status: 'success',
      },
    ],
  },
  {
    id: 3,
    name: '名称3',
    qrcode: "",
    desc: '系统性的沉淀B端知识体系',
    content: [
      {
        label: '今日订单数',
        value: 2903,
      },
      {
        label: '今日金额',
        value: 3720,
      },
      {
        label: '总订单数',
        value: 3720,
      },
      {
        label: '总金额',
        value: 3720,
      },
      {
        label: '状态',
        value: '启用',
        status: 'success',
      },
    ],
  },
];


const renderBadge = (count: number, active = false) => {
  return (
    <Badge
      count={count}
      style={{
        marginBlockStart: -2,
        marginInlineStart: 4,
        color: active ? '#1890FF' : '#999',
        backgroundColor: active ? '#E6F7FF' : '#eee',
      }}
    />
  );
};
const waitTime = (time: number = 100) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(true);
    }, time);
  });
};
const AddPayQRCode = ({modalVisit, setModalVisit, info}: {
  modalVisit: any,
  setModalVisit: any,
  info: { name: string; qrcode: string }
}) => {
  console.log("info", info)
  const [form] = Form.useForm<{ name: string; qrcode: string }>();
  form.setFieldsValue(info)

  return (
    <ModalForm<{
      name: string;
      qrcode: string;
    }>
      title="新建表单"
      open={modalVisit}
      onOpenChange={setModalVisit}
      form={form}
      autoFocusFirstInput
      modalProps={{
        destroyOnClose: true,
        onCancel: () => console.log('run'),
      }}
      submitTimeout={2000}
      onFinish={async (values) => {
        if (info) {

        }
        await waitTime(2000);
        console.log(values.name);
        message.success('提交成功');
        return true;
      }}
    >
      <ProFormText
        name="name"
        width="md"
        label="项目名称"
        initialValue="xxxx项目"
      />
      <ProFormUploadDragger name="qrcode_up" label="拖拽上传"/>
    </ModalForm>
  );
};
const PaymentPlatform: React.FC = () => {
  const [activeKey, setActiveKey] = useState<React.Key | undefined>('tab1');
  const action = useRef<ActionType>();
  const [modalVisit, setModalVisit] = useState(false);
  const [editData, setEditData] = useState({});

  return (
    <>
      <AddPayQRCode modalVisit={modalVisit} setModalVisit={setModalVisit} info={editData}/>
      <ProList<any>
        rowKey="name"
        actionRef={action}
        dataSource={dataSource}
        editable={{}}
        metas={{
          title: {
            dataIndex: 'name',
            valueType: 'select',
          },
          description: {
            key: 'desc',
          },
          content: {
            dataIndex: 'content',
            render: (text) => (
              <div
                key="label"
                style={{display: 'flex', justifyContent: 'space-around'}}
              >
                {(text as any[]).map((t) => (
                  <div key={t.label}>
                    <div>{t.label}</div>
                    <div>
                      {t.status === 'success' && (
                        <span
                          style={{
                            display: 'inline-block',
                            width: 8,
                            height: 8,
                            borderRadius: '50%',
                            backgroundColor: '#52c41a',
                            marginInlineEnd: 8,
                          }}
                        />
                      )}
                      {t.value}
                    </div>
                  </div>
                ))}
              </div>
            ),
          },
          actions: {
            render: (text, row) => [
              <a
                href={row.html_url}
                target="_blank"
                rel="noopener noreferrer"
                key="link"
                onClick={() => {
                  setEditData(row);
                  setModalVisit(true);
                  // action.current?.startEditable(row.name);
                }}
              >
                编辑
              </a>,
              <a target="_blank" rel="noopener noreferrer" key="error">
                禁用
              </a>,
              <a target="_blank" rel="noopener noreferrer" key="view" className="text-red-500">
                删除
              </a>,
            ],
          },
        }}
        toolbar={{
          menu: {
            activeKey,
            items: [
              {
                key: 'tab1',
                label: (
                  <span>微信{renderBadge(1, activeKey === 'tab1')}</span>
                ),
              },
              {
                key: 'tab2',
                label: (
                  <span>
                  支付宝{renderBadge(2, activeKey === 'tab2')}
                </span>
                ),
              },
            ],
            onChange(key) {
              setActiveKey(key);
            },
          },
          actions: [
            <Button type="primary" key="primary" onClick={() => {
              setEditData({});
              setModalVisit(true);
            }}
            >
              新建
            </Button>,
          ],
        }}
      />
    </>
  );
};


const Admin: React.FC = () => {

  return (
    <PageContainer>
      <PaymentPlatform/>
    </PageContainer>
  );
};

export default Admin;
