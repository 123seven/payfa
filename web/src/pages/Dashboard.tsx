import {PageContainer, ProCard, StatisticCard} from '@ant-design/pro-components';
import {useModel} from '@umijs/max';
import {Card, Statistic, theme} from 'antd';
import React, {useState} from 'react';
import RcResizeObserver from 'rc-resize-observer';

type statisticInfoType = { today_orders: number; today_amount: number; all_orders: number; all_amount: number; };

const StatisticData: React.FC = () => {
  const info: statisticInfoType = {
    today_orders: 1,
    today_amount: 1,
    all_orders: 1,
    all_amount: 1,
  }

  const [responsive, setResponsive] = useState(false);


  return (<RcResizeObserver
      key="resize-observer"
      onResize={(offset) => {
        setResponsive(offset.width < 596);
      }}
    >
      <ProCard
        title="数据概览"
        extra="2019年9月28日 星期五"
        split={responsive ? 'horizontal' : 'vertical'}
        headerBordered
        bordered
      >
        <ProCard split="horizontal">
          <ProCard split="horizontal">
            <ProCard split="vertical">
              <StatisticCard
                statistic={{
                  title: '昨日全部流量',
                  value: 234,
                  description: (
                    <Statistic
                      title="较本月平均流量"
                      value="8.04%"
                      trend="down"
                    />
                  ),
                }}
              />
              <StatisticCard
                statistic={{
                  title: '本月累计流量',
                  value: 234,
                  description: (
                    <Statistic title="月同比" value="8.04%" trend="up"/>
                  ),
                }}
              />
            </ProCard>
            <ProCard split="vertical">
              <StatisticCard
                statistic={{
                  title: '运行中实验',
                  value: '12/56',
                  suffix: '个',
                }}
              />
              <StatisticCard
                statistic={{
                  title: '历史实验总数',
                  value: '134',
                  suffix: '个',
                }}
              />
            </ProCard>
          </ProCard>
          <StatisticCard
            title="流量走势"
            chart={
              <img
                src="https://gw.alipayobjects.com/zos/alicdn/_dZIob2NB/zhuzhuangtu.svg"
                width="100%"
              />
            }
          />
        </ProCard>
        <StatisticCard
          title="流量占用情况"
          chart={
            <img
              src="https://gw.alipayobjects.com/zos/alicdn/qoYmFMxWY/jieping2021-03-29%252520xiawu4.32.34.png"
              alt="大盘"
              width="100%"
            />
          }
        />
      </ProCard>
    </RcResizeObserver>
  )
};

const Dashboard: React.FC = () => {
  const {token} = theme.useToken();
  const {initialState} = useModel('@@initialState');

  return (
    <PageContainer>
      <Card
        style={{
          borderRadius: 8,
        }}
        bodyStyle={{
          backgroundImage:
            initialState?.settings?.navTheme === 'realDark'
              ? 'background-image: linear-gradient(75deg, #1A1B1F 0%, #191C1F 100%)'
              : 'background-image: linear-gradient(75deg, #FBFDFF 0%, #F5F7FF 100%)',
        }}
      >
        <div
          style={{
            backgroundPosition: '100% -30%',
            backgroundRepeat: 'no-repeat',
            backgroundSize: '274px auto',
            backgroundImage:
              "url('https://gw.alipayobjects.com/mdn/rms_a9745b/afts/img/A*BuFmQqsB2iAAAAAAAAAAAAAAARQnAQ')",
          }}
        >
          <div
            style={{
              fontSize: '20px',
              color: token.colorTextHeading,
            }}
          >
            欢迎使用 MoDo(米多)
          </div>
          <p
            style={{
              fontSize: '14px',
              color: token.colorTextSecondary,
              lineHeight: '22px',
              marginTop: 16,
              marginBottom: 32,
              width: '65%',
            }}
          >
            MoDo 是个人小额低频收款方案。致力于在。
          </p>
          <StatisticData/>
        </div>
      </Card>
    </PageContainer>
  );
};

export default Dashboard;
